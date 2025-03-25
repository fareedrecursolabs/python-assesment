import uuid
import pytest
from datetime import datetime
from django.utils.timezone import make_aware
from github_commits.models import Commit
from github_branches.models import Branch
from github_repos.models import GithubRepo
from github_commits.serializer import CommitsSerializer
from github_repos.serializer import RepoSerializer
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_commit_serialization(commit):
    """Test if Commit model instance serializes correctly"""
    serializer = CommitsSerializer(commit)
    data = serializer.data

    assert data["id"] == str(commit.id)  # UUID is serialized as a string
    assert data["message"] == commit.message
    assert data["pushed_at"] == commit.pushed_at.isoformat().replace("+00:00", "Z")
    assert data["modified_files"] == commit.modified_files
    assert data["author_name"] == commit.author_name
    assert data["author_email"] == commit.author_email
    assert data["author_username"] == commit.author_username
    assert data["branch"] == commit.branch.id  # ForeignKey should be serialized as ID


@pytest.mark.django_db
def test_commit_deserialization(branch):
    """Test deserialization and saving a commit"""
    commit_data = {
        "id": str(uuid.uuid4()),
        "message": "New commit",
        "pushed_at": make_aware(datetime(2024, 3, 25, 10, 0)).isoformat(),
        "modified_files": ["file1.py", "file2.js"],
        "author_name": "John Doe",
        "author_email": "johndoe@example.com",
        "author_username": "johndoe123",
        "branch": branch.id  # Provide existing branch ID
    }

    serializer = CommitsSerializer(data=commit_data)
    assert serializer.is_valid(), serializer.errors  # Ensure the serializer validates the data

    commit_instance = serializer.save()
    assert commit_instance.message == commit_data["message"]
    assert commit_instance.pushed_at.isoformat() == commit_data["pushed_at"]
    assert commit_instance.modified_files == commit_data["modified_files"]
    assert commit_instance.branch == branch  # Ensure branch association


@pytest.mark.django_db
def test_invalid_commit_deserialization():
    """Test validation errors when required fields are missing"""
    invalid_data = {
        "message": "Invalid commit"
        # Missing required fields like `pushed_at`, `branch`, etc.
    }

    serializer = CommitsSerializer(data=invalid_data)
    assert not serializer.is_valid()  # Should fail validation
    assert "pushed_at" in serializer.errors  # Expect missing field error
    assert "branch" in serializer.errors  # ForeignKey is required
