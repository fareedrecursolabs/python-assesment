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
        "main_branch": repository.get("default_branch", ""),
    }

    serializer = RepoSerializer(data=formatted_data)
    if serializer.is_valid():
        GithubRepo.objects.update_or_create(
            id=formatted_data["id"], defaults=formatted_data
        )
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
    html_url: str = pull_request.get("html_url", "")
    number: int = pull_request.get("number", None)

    try:
        repo = GithubRepo.objects.get(id=repo_id)
        branch = Branch.objects.get(
            repo_id=repo_id, name=pull_request.get("head", {}).get("ref", "")
        )
    except GithubRepo.DoesNotExist:
        print(f"❌ Repo with ID {repo_id} not found")
        return None
    except Branch.DoesNotExist:
        print(f"❌ Branch not found for repo ID {repo_id}")
        return None

    formatted_data = {
        "title": pull_request.get("title", ""),
        "body": pull_request.get("body", ""),
        "state": (
            "merged" if pull_request.get("merged") else pull_request.get("state", "")
        ),
        "base_branch": pull_request.get("base", {}).get("ref", ""),
        "head_branch": pull_request.get("head", {}).get("ref", ""),
        "url": url,
        "html_url": html_url,
        "number": number,
        "commits": pull_request.get("commits", 0),
        "additions": pull_request.get("additions", 0),
        "deletions": pull_request.get("deletions", 0),
        "changed_files": pull_request.get("changed_files", 0),
        "user": pull_request.get("user", {}).get("login", ""),
        "created_at": pull_request.get("created_at", None),
        "updated_at": pull_request.get("updated_at", None),
        "closed_at": pull_request.get("closed_at", None),
        "merged_at": pull_request.get("merged_at", None),
        "repo": repo_id,
        "branch": branch.id,
    }

    serializer = PullRequestSerializer(data=formatted_data)
    if serializer.is_valid():
        pull_request_obj, _ = PullRequest.objects.update_or_create(
            url=url,
            defaults={
                "title": formatted_data["title"],
                "body": formatted_data["body"],
                "state": formatted_data["state"],
                "base_branch": formatted_data["base_branch"],
                "head_branch": formatted_data["head_branch"],
                "html_url": formatted_data["html_url"],
                "number": formatted_data["number"],
                "commits": formatted_data["commits"],
                "additions": formatted_data["additions"],
                "deletions": formatted_data["deletions"],
                "changed_files": formatted_data["changed_files"],
                "user": formatted_data["user"],
                "created_at": formatted_data["created_at"],
                "updated_at": formatted_data["updated_at"],
                "closed_at": formatted_data["closed_at"],
                "merged_at": formatted_data["merged_at"],
                "repo": repo,
                "branch": branch,
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
