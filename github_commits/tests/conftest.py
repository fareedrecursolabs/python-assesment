import pytest
import uuid
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework.test import APIClient
from github_commits.models import Commit
from github_branches.models import Branch
from github_repos.models import GithubRepo


@pytest.fixture
def api_client():
    """Fixture for Django REST Framework API client"""
    return APIClient()


@pytest.fixture
def repo(db):
    """Create a test repository"""
    return GithubRepo.objects.create(
        id=uuid.uuid4().int & (1 << 63) - 1,  # Ensure a valid BigInteger ID dynamically
        name="Test Repo",
        url="https://github.com/test/repo",
        owner_name="Test Owner",
        owner_email="test@example.com",
        main_branch="main"
    )


@pytest.fixture
def branch(repo):
    """Create a test branch"""
    return Branch.objects.create(
        id=uuid.uuid4(),
        name="feature-branch",
        repo=repo
    )


@pytest.fixture
def commit(branch):
    """Create a test commit"""
    return Commit.objects.create(
        id=uuid.uuid4(),
        message="Initial commit",
        pushed_at=make_aware(datetime(2024, 3, 24, 12, 0)),
        modified_files=[],  # Explicitly setting this to None
        author_name="test_user",
        author_email="test@example.com",
        author_username="testuser123",
        branch=branch  # Can also test with branch=None if needed
    )
