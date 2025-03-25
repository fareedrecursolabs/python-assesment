import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from github_commits.models import Commit


@pytest.mark.django_db
def test_list_commits(api_client, branch, commit):
    """Test retrieving a list of commits for a specific branch"""
    url = reverse('commits_list', kwargs={'branch_id': branch.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Only one commit created
    assert response.data[0]["id"] == str(commit.id)  # Convert UUID to string
    assert response.data[0]["message"] == commit.message
    assert str(response.data[0]["branch"]) == str(branch.id)  # Ensure both are strings


@pytest.mark.django_db
def test_list_commits_empty(api_client, branch):
    """Test retrieving commits when no commits exist for the branch"""
    url = reverse('commits_list', kwargs={'branch_id': branch.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []  # No commits should be returned


@pytest.mark.django_db
def test_retrieve_commit(api_client, branch, commit):
    """Test retrieving a specific commit by ID"""
    url = reverse('commits_detail', kwargs={'branch_id': branch.id, 'pk': commit.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(commit.id)  # Convert UUID to string
    assert response.data["message"] == commit.message
    assert str(response.data["branch"]) == str(branch.id)  # Ensure both are strings


@pytest.mark.django_db
def test_retrieve_nonexistent_commit(api_client, branch):
    """Test retrieving a commit that does not exist"""
    fake_commit_id = uuid.uuid4()
    url = reverse('commits_detail', kwargs={'branch_id': branch.id, 'pk': fake_commit_id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_retrieve_commit_wrong_branch(api_client, branch, commit, repo):
    """Test retrieving a commit that belongs to a different branch"""
    # Create a new branch not associated with the commit
    another_branch = branch.__class__.objects.create(id=uuid.uuid4(), name="new-branch", repo=repo)

    url = reverse('commits_detail', kwargs={'branch_id': another_branch.id, 'pk': commit.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND  # Commit doesn't belong to this branch
