from uuid import UUID
from celery import shared_task
from .service import createBranch, createCommit, createPullRequest, createRepository
from django.views.decorators.csrf import csrf_exempt

@shared_task
def process_github_webhook(data):
    """Celery task to process GitHub webhook asynchronously"""
    repository = data.get("repository")
    pull_request = data.get("pull_request")

    print(repository)

    if not repository:
        return "No repository data found"

    repo_id: int = repository.get("id")
    branch_id: UUID = None
    commits = data.get("commits")

    createRepository(repository)

    if data.get("ref"):
        branch_id = createBranch(data, repo_id)

    if pull_request:
        createPullRequest(pull_request, repo_id)

    if commits and isinstance(commits, list) and len(commits) > 0:
        createCommit(commits, branch_id)

    return "Webhook processed successfully"
