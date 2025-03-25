import pytest
from github_pull_requests.serializer import PullRequestSerializer

def test_pull_request_serializer_valid_data(pull_request):
    """Test PullRequestSerializer with valid pull request instance"""
    serializer = PullRequestSerializer(instance=pull_request)
    data = serializer.data

    assert data['id'] == str(pull_request.id)
    assert data['title'] == pull_request.title
    assert data['body'] == pull_request.body
    assert data['state'] == pull_request.state
    assert data['base_branch'] == pull_request.base_branch
    assert data['head_branch'] == pull_request.head_branch
    assert data['url'] == pull_request.url
    assert data['html_url'] == pull_request.html_url
    assert data['number'] == pull_request.number
    assert data['commits'] == pull_request.commits
    assert data['additions'] == pull_request.additions
    assert data['deletions'] == pull_request.deletions
    assert data['changed_files'] == pull_request.changed_files
    assert data['user'] == pull_request.user
    assert data['created_at'] == pull_request.created_at.isoformat().replace("+00:00", "Z")
    assert data['updated_at'] == pull_request.updated_at.isoformat().replace("+00:00", "Z")
    assert data['closed_at'] is None  # Ensuring null fields are handled correctly
    assert data['merged_at'] is None
    assert data['repo'] == pull_request.repo.id  # ForeignKey field
    assert data['branch']['name'] == pull_request.branch.name  # Nested serializer field

def test_pull_request_serializer_invalid_data():
    """Test PullRequestSerializer with invalid data"""
    invalid_data = {
        "title": "",  # Title is required
        "state": "",  # State is required
        "base_branch": "",
        "head_branch": "",
        "url": "invalid-url",  # URL should be a valid URL
        "html_url": "invalid-url",
        "user": ""
    }
    serializer = PullRequestSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors
    assert "state" in serializer.errors
    assert "url" in serializer.errors
    assert "html_url" in serializer.errors

def test_pull_request_serializer_partial_update(pull_request):
    """Test partial update of PullRequestSerializer"""
    partial_data = {"title": "Updated Title"}
    serializer = PullRequestSerializer(instance=pull_request, data=partial_data, partial=True)
    assert serializer.is_valid()
    updated_instance = serializer.save()
    assert updated_instance.title == "Updated Title"
