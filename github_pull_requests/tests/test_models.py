import pytest
from django.core.exceptions import ValidationError
from github_pull_requests.models import PullRequest


@pytest.mark.django_db
def test_pull_request_creation(pull_request):
    """Test if PullRequest instance is created successfully"""
    assert pull_request.title == "Fix Bug"
    assert pull_request.body == "Fixing a critical issue"
    assert pull_request.state == "open"
    assert pull_request.base_branch == "main"
    assert pull_request.head_branch == "feature-1"
    assert pull_request.url == "https://github.com/test/repo/pull/1"
    assert pull_request.html_url == "https://github.com/test/repo/pull/1"
    assert pull_request.number == 1
    assert pull_request.commits == 3
    assert pull_request.additions == 10
    assert pull_request.deletions == 2
    assert pull_request.changed_files == 1
    assert pull_request.user == "test_user"
    assert pull_request.created_at is not None
    assert pull_request.updated_at is not None
    assert pull_request.closed_at is None  # Nullable field
    assert pull_request.merged_at is None  # Nullable field
    assert pull_request.repo is not None  # ForeignKey must be assigned in fixture
    assert pull_request.branch is not None  # ForeignKey must be assigned in fixture


@pytest.mark.django_db
def test_string_representation(pull_request):
    """Test the __str__ method"""
    assert str(pull_request) == f"{pull_request.title} ({pull_request.state})"
