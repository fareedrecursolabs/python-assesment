import pytest


@pytest.mark.django_db
def test_model_str(repo1):
    """Test the string representation of the GithubRepo model"""
    assert str(repo1) == "Repo One"
