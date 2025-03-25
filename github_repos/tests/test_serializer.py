import pytest
from github_repos.serializer import RepoSerializer


@pytest.mark.django_db
def test_valid_serializer(repo1):
    """Test serializer with valid data"""
    serializer = RepoSerializer(instance=repo1)
    expected_data = {
        "id": repo1.id,
        "name": repo1.name,
        "url": repo1.url,
        "owner_name": repo1.owner_name,
        "owner_email": repo1.owner_email,
        "main_branch": repo1.main_branch,
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_invalid_serializer():
    """Test serializer with missing required fields"""
    invalid_data = {"id": 9999}  # Missing required fields
    serializer = RepoSerializer(data=invalid_data)

    assert not serializer.is_valid()  # Serializer should fail validation
    assert "name" in serializer.errors
    assert "url" in serializer.errors
    assert "owner_name" in serializer.errors
    assert "owner_email" in serializer.errors
    assert "main_branch" in serializer.errors
