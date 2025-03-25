import pytest
import uuid
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework.test import APIClient
from github_repos.models import GithubRepo
from github_branches.models import Branch
from github_pull_requests.models import PullRequest


@pytest.fixture
def api_client():
    """Fixture for Django REST Framework API client"""
    return APIClient()


@pytest.fixture
def repo(db):
    """Create a test repository"""
    return GithubRepo.objects.create(
        id=123456,
        name="Test Repo",
        url="https://github.com/test/repo",
        owner_name="Test Owner",
        owner_email="test@example.com",
        main_branch="main"
    )


@pytest.fixture
def branch(repo):
    """Create a test branch"""
    return Branch.objects.create(name="feature-1", repo=repo)


@pytest.fixture
def pull_request(repo, branch):
    """Create a test pull request"""
    return PullRequest.objects.create(
        id=uuid.uuid4(),
        title="Fix Bug",
        body="Fixing a critical issue",
        state="open",
        base_branch="main",
        head_branch="feature-1",
        url="https://github.com/test/repo/pull/1",
        html_url="https://github.com/test/repo/pull/1",
        number=1,
        commits=3,
        additions=10,
        deletions=2,
        changed_files=1,
        user="test_user",
        created_at=make_aware(datetime(2024, 3, 24, 12, 0)),
        updated_at=make_aware(datetime(2024, 3, 25, 12, 0)),
        closed_at=None,  # Explicitly setting null values
        merged_at=None,
        repo=repo,
        branch=branch
    )
