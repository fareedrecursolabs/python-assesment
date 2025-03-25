import pytest
from github_branches.serializer import BranchSerializer
from github_branches.models import Branch  # Fix relative import issue
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_branch_serialization(branch1):
    """Test that the serializer correctly serializes a Branch instance"""
    serializer = BranchSerializer(instance=branch1)
    expected_data = {
        "id": str(branch1.id),  # Ensure UUID is serialized as string
        "name": branch1.name,
        "repo": branch1.repo.id  # ForeignKey should be represented by ID
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_branch_deserialization_valid(repo):
    """Test deserialization of valid data"""
    data = {
        "name": "new-branch",
        "repo": repo.id
    }
    serializer = BranchSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "new-branch"
    assert serializer.validated_data["repo"] == repo


@pytest.mark.django_db
def test_branch_deserialization_missing_name(repo):
    """Test validation error when 'name' is missing"""
    data = {
        "repo": repo.id
    }
    serializer = BranchSerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors  # Name is required



@pytest.mark.django_db
def test_cannot_create_branch_without_repo():
    """Test that a branch cannot be created without a repository"""
    with pytest.raises(IntegrityError):  # Expect an IntegrityError due to FK constraint
        Branch.objects.create(name="orphan-branch", repo=None)
