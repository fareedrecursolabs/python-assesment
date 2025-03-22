from typing import Optional, List, Dict, Any
from uuid import UUID
from rest_framework.response import Response
from rest_framework import status
from github_commits.serializer import CommitsSerializer
from github_repos.serializer import RepoSerializer
from github_repos.models import GithubRepo
from github_branches.serializer import BranchSerializer
from github_branches.models import Branch
from github_pull_requests.serializer import PullRequestSerializer
from github_pull_requests.models import PullRequest

class RepositoryData(Dict[str, Any]):
    id: int
    name: Optional[str]
    owner_name: Optional[str]
    owner_email: Optional[str]
    url: Optional[str]


def createRepository(repository: Dict[str, Any]) -> None:
    formatted_data: RepositoryData = {
        "id": repository.get("id", 0),  # Ensure ID is always an int
        "name": repository.get("name", ""),
        "owner_name": repository.get("owner", {}).get("name"),
        "owner_email": repository.get("owner", {}).get("email"),
        "url": repository.get("git_url", ""),
    }

    serializer = RepoSerializer(data=formatted_data)
    if serializer.is_valid():
        GithubRepo.objects.update_or_create(id=formatted_data["id"], defaults=formatted_data)
    else:
        print("Serializer errors:", serializer.errors)


def createCommit(commits: List[Dict[str, Any]], branch_id: Optional[UUID]) -> Response:
    for commit in commits:
        formatted_data = {
            "id": commit.get("id", ""),
            "message": commit.get("message", ""),
            "pushed_at": commit.get("timestamp", ""),
            "author_name": commit.get("committer", {}).get("name", ""),
            "author_email": commit.get("committer", {}).get("email", ""),
            "author_username": commit.get("committer", {}).get("username", ""),
            "commit_url": commit.get("url", ""),
            "branch": branch_id,  # ✅ Ensure branch_id is Optional[UUID]
            "modified_files": commit.get("modified", []),
        }

        serializer = CommitsSerializer(data=formatted_data)
        if serializer.is_valid():
            serializer.save()
        else:
            print("Serializer errors:", serializer.errors)

    return Response(status=status.HTTP_201_CREATED)


def createPullRequest(pull_request: Dict[str, Any], repo_id: int) -> Optional[Response]:
    url: str = pull_request.get("url", "")

    try:
        repo = GithubRepo.objects.get(id=repo_id)
    except GithubRepo.DoesNotExist:
        print(f"❌ Repo with ID {repo_id} not found")
        return None

    formatted_data = {
        "title": pull_request.get("title", ""),
        "created_at": pull_request.get("created_at", ""),
        "user": pull_request.get("user", {}).get("login", ""),
        "url": url,
        "state": "merged" if pull_request.get("merged") else pull_request.get("state", ""),
        "repo": repo_id,
    }

    serializer = PullRequestSerializer(data=formatted_data)
    if serializer.is_valid():
        PullRequest.objects.update_or_create(
            url=url,
            defaults={
                "title": pull_request.get("title", ""),
                "created_at": pull_request.get("created_at", ""),
                "user": pull_request.get("user", {}).get("login", ""),
                "url": url,
                "state": "merged" if pull_request.get("merged") else pull_request.get("state", ""),
                "repo": repo,
            },
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Serializer errors:", serializer.errors)
        return None


def createBranch(data: Dict[str, Any], repo_id: int) -> Optional[UUID]:
    branch_name: str = data.get("ref", "").split("/")[-1]

    try:
        repo = GithubRepo.objects.get(id=repo_id)
    except GithubRepo.DoesNotExist:
        print(f"❌ Repo with ID {repo_id} not found")
        return None

    formatted_data = {"name": branch_name, "repo": repo.id}

    serializer = BranchSerializer(data=formatted_data)
    if serializer.is_valid():
        branch, _ = Branch.objects.update_or_create(
            name=branch_name, repo=repo, defaults={"name": branch_name, "repo": repo}
        )
        return branch.id
    else:
        print("Serializer errors:", serializer.errors)
        return None
