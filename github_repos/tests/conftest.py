import pytest
from rest_framework.test import APIClient
from github_repos.models import GithubRepo


@pytest.fixture
def api_client():
    """Fixture for Django REST Framework API client."""
    return APIClient()


@pytest.fixture
def repo1(db):
    """Creates and returns a test GitHub repository (Repo One)."""
    return GithubRepo.objects.create(
        id=1001,  # BigIntegerField primary key
        name="Repo One",
        url="https://github.com/repo1",
        owner_name="Alice",
        owner_email="alice@example.com",
        main_branch="main"
    )


@pytest.fixture
def repo2(db):
    """Creates and returns another test GitHub repository (Repo Two)."""
    return GithubRepo.objects.create(
        id=1002,
        name="Repo Two",
        url="https://github.com/repo2",
        owner_name="Bob",
        owner_email="bob@example.com",
        main_branch="develop"
    )
