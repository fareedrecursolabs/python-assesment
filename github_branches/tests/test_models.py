import pytest
from django.core.exceptions import ValidationError
from github_branches.models import Branch
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_branch_creation(branch1, repo):
    """Test if the Branch instance is created successfully"""
    assert branch1.name == "feature-1"
    assert branch1.repo == repo


@pytest.mark.django_db
def test_string_representation(branch1):
    """Test the __str__ method"""
    assert str(branch1) == "feature-1 (Test Repo)"

@pytest.mark.django_db
def test_branch_without_repo_fails(db):
    """Test that branch creation without a repo should fail"""
    with pytest.raises(IntegrityError):
        Branch.objects.create(name="standalone-branch", repo=None)


@pytest.mark.django_db
def test_missing_required_fields(db):
    """Test that missing required fields raise validation errors"""
    with pytest.raises(ValidationError):
        branch = Branch(name="")  # Name is required
        branch.full_clean()  # Triggers Django's model validation


@pytest.mark.django_db
def test_foreign_key_cascade(repo, branch1):
    """Test foreign key constraints (repo deletion should delete branch)"""
    repo.delete()
    with pytest.raises(Branch.DoesNotExist):
        Branch.objects.get(id=branch1.id)
