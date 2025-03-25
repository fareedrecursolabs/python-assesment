import pytest
from rest_framework.test import APIClient
from github_repos.models import GithubRepo
from github_branches.models import Branch


@pytest.fixture
def api_client():
    """Fixture for API test client"""
    return APIClient()


@pytest.fixture
def repo(db):
    """Fixture for a test GitHub repository"""
    return GithubRepo.objects.create(
        id=123456,
        name="Test Repo",
        url="https://github.com/test/repo",
        owner_name="Test Owner",
        owner_email="test@example.com",
        main_branch="main"
    )


@pytest.fixture
def other_repo(db):
    """Fixture for another test repository"""
    return GithubRepo.objects.create(
        id=789012,
        name="Other Repo",
        url="https://github.com/other/repo",
        owner_name="Other Owner",
        owner_email="other@example.com",
        main_branch="dev"
    )


@pytest.fixture
def branch1(db, repo):
    """Fixture for the first branch of the test repo"""
    return Branch.objects.create(name="feature-1", repo=repo)


@pytest.fixture
def branch2(db, repo):
    """Fixture for the second branch of the test repo"""
    return Branch.objects.create(name="feature-2", repo=repo)


@pytest.fixture
def other_branch(db, other_repo):
    """Fixture for a branch in the other repo"""
    return Branch.objects.create(name="other-branch", repo=other_repo)
