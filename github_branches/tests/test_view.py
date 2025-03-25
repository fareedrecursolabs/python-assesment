import pytest
from django.urls import reverse
from rest_framework import status
import uuid  # Import UUID for generating valid test UUIDs


@pytest.mark.django_db
def test_list_branches(api_client, repo, branch1, branch2):
    """Test retrieving all branches for a specific repository"""
    url = reverse("branch_list", kwargs={"repo_id": repo.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)  # Ensure response is a list
    assert len(response.data) == 2  # Should return two branches


@pytest.mark.django_db
def test_list_branches_empty(api_client):
    """Test retrieving branches when no branches exist for the repo"""
    url = reverse("branch_list", kwargs={"repo_id": 999999})  # Non-existent repo
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)  # Ensure response is a list
    assert len(response.data) == 0  # Should return empty list


@pytest.mark.django_db
def test_get_branch_details(api_client, repo, branch1):
    """Test retrieving a specific branch"""
    url = reverse("branch_detail", kwargs={"repo_id": repo.id, "pk": str(branch1.id)})  # Ensure UUID is a string
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == branch1.name


@pytest.mark.django_db
def test_get_branch_details_invalid(api_client, repo):
    """Test retrieving a non-existent branch"""
    fake_uuid = str(uuid.uuid4())  # Generate a random valid UUID
    url = reverse("branch_detail", kwargs={"repo_id": repo.id, "pk": fake_uuid})  # Invalid branch ID
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND  # Should return 404 for non-existent branch
