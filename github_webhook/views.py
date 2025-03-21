from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from github_commits.serializer import CommitsSerializer
from rest_framework import status
from github_repos.serializer import RepoSerializer
from github_repos.models import GithubRepo
from github_branches.serializer import BranchSerializer
from github_branches.models import Branch
from github_pull_requests.serializer import PullRequestSerializer
from github_pull_requests.models import PullRequest
from uuid import uuid4


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def github_webhook(request):
    print("isinstance(commits, list)", isinstance(request.data, list), request.data)
    repository = request.data.get("repository")
    pull_request = request.data.get("pull_request")
    repo_id: int = repository.get("id")
    branch_id: uuid4 = None
    commits = request.data.get("commits")
    if repository:
        createRepository(repository)
        if request.data.get("ref"):
            branch_id = createBranch(request.data, repo_id)
        if pull_request:
            createPullRequest(pull_request, repo_id)
        if commits and isinstance(commits, list) and len(commits) > 0:
            createCommit(commits, branch_id)
    return Response({"message": "Webhook received successfully"}, status=200)


def createRepository(repository) -> None:
    formatted_data = {
        "id": repository.get("id"),
        "name": repository.get("name"),
        "owner_name": repository.get("owner", {}).get("name"),
        "owner_email": repository.get("owner", {}).get("email"),
        "url": repository.get("git_url"),
    }
    serializer = RepoSerializer(data=formatted_data)
    if serializer.is_valid():
        repository, created = GithubRepo.objects.update_or_create(
            id=repository.get("id"), defaults=formatted_data
        )
    else:
        print("Serializer errors:", serializer.errors)


def createCommit(commits, branch_id):
    for commit in commits:
        formatted_data = {
            "id": commit.get("id"),
            "message": commit.get("message"),
            "pushed_at": commit.get("timestamp"),
            "author_name": commit.get("committer", {}).get("name"),
            "author_email": commit.get("committer", {}).get("email"),
            "author_username": commit.get("committer", {}).get("username"),
            "commit_url": commit.get("url"),
            "branch": branch_id,
            "modified_files": commit.get("modified", []),
        }
        serializer = CommitsSerializer(data=formatted_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)


def createPullRequest(pull_request, repo_id) -> None:
    url: str = pull_request.get("url")
    repo = GithubRepo.objects.get(id=repo_id)
    formatted_data = {
        "title": pull_request.get("title"),
        "created_at": pull_request.get("created_at"),
        "user": pull_request.get("user", {}).get("login"),
        "url": url,
        "state": pull_request.get("state"),
        "repo": repo_id,
    }
    serializer = PullRequestSerializer(data=formatted_data)
    if serializer.is_valid():
        branch, created = PullRequest.objects.update_or_create(
            url=url,
            defaults={
                "title": pull_request.get("title"),
                "created_at": pull_request.get("created_at"),
                "user": pull_request.get("user", {}).get("login"),
                "url": url,
                "state": pull_request.get("state"),
                "repo": repo,
            },
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Serializer errors:", serializer.errors)


def createBranch(data, repo_id) -> uuid4:
    branch_name: str = data.get("ref").split("/")[-1]
    repo = GithubRepo.objects.get(id=repo_id)
    formatted_data = {"name": branch_name, "repo": repo.id}
    serializer = BranchSerializer(data=formatted_data)
    if serializer.is_valid():
        branch, created = Branch.objects.update_or_create(
            name=branch_name, repo=repo, defaults={"name": branch_name, "repo": repo}
        )
        return branch.id  # Return branch ID
    else:
        print("Serializer errors:", serializer.errors)
        return None
