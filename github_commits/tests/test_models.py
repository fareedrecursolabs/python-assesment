import uuid
import pytest
from github_commits.models import Commit
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from datetime import datetime
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_commit_creation(commit, branch):
    """Test if a commit instance is created successfully"""
    assert commit.message == "Initial commit"
    assert commit.branch == branch
    assert commit.author_username == "testuser123"  # Fixed expected username


@pytest.mark.django_db
def test_commit_string_representation(commit):
    """Test the __str__ method of the Commit model"""
    expected_str = f"{commit.message} {commit.branch.name}"
    assert str(commit) == expected_str


@pytest.mark.django_db
def test_commit_without_branch():
    """Test should only run if 'branch' is nullable"""
    with pytest.raises(IntegrityError):
        Commit.objects.create(
            id=uuid.uuid4(),
            message="Orphan commit",
            author_name="test_user",
            author_email="test@example.com",
            modified_files=[],  # Use list instead of dict to match model
            pushed_at=make_aware(datetime(2024, 3, 24, 14, 0)),  # Required field
            branch=None  # No branch
        )


@pytest.mark.django_db
def test_commit_missing_fields():
    """Test commit creation with missing optional fields"""
    with pytest.raises(ValidationError):
        commit = Commit(id=uuid.uuid4())
        commit.full_clean()  # Ensure validation catches missing required fields


@pytest.mark.django_db
def test_commit_foreign_key_constraints(commit, branch):
    """Test that a commit is deleted when the related branch is deleted"""
    branch.delete()
    assert not Commit.objects.filter(id=commit.id).exists()


@pytest.mark.django_db
def test_commit_validation_error():
    """Test validation error when an invalid value is assigned"""
    commit = Commit(
        id=uuid.uuid4(),
        message="A" * 300,  # Exceeds 255 characters
        pushed_at=make_aware(datetime(2024, 3, 24, 15, 0)),  # Required field
        modified_files=[],
        author_name="test_user",
        author_email="test@example.com",
        author_username="testuser123",
        branch=None
    )

    with pytest.raises(ValidationError):
        commit.full_clean()  # This should raise an error due to the long message
