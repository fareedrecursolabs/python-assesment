import pytest
from django.urls import reverse
from rest_framework import status
from github_repos.models import GithubRepo


@pytest.mark.django_db
def test_get_repo_list(api_client, repo1, repo2):
    """Test retrieving the list of repositories"""
    url = reverse("repo_list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Should return both repositories
    assert response.data[0]["name"] == "Repo One"


@pytest.mark.django_db
def test_get_repo_details(api_client, repo1):
    """Test retrieving a single repository"""
    url = reverse("repo_detail", args=[repo1.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Repo One"


@pytest.mark.django_db
def test_get_invalid_repo(api_client):
    """Test retrieving a non-existent repository should return 404"""
    url = reverse("repo_detail", args=[9999])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
