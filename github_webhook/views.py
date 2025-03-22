import hashlib
import hmac
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .service import createBranch, createCommit, createPullRequest, createRepository
from uuid import UUID

SECRET_TOKEN = os.getenv("GITHUB_WEBHOOK_SECRET")

def verify_github_signature(request):
    """Verify the X-Hub-Signature-256 header to authenticate GitHub webhook requests"""
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        return False

    mac = hmac.new(
        SECRET_TOKEN.encode(),
        msg=request.body,
        digestmod=hashlib.sha256
    )
    expected_signature = f"sha256={mac.hexdigest()}"

    return hmac.compare_digest(expected_signature, signature)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def github_webhook(request):

    if not verify_github_signature(request):
        return Response({"error": "Unauthorized"}, status=401)

    repository = request.data.get("repository")
    print(repository)
    pull_request = request.data.get("pull_request")
    repo_id: int = repository.get("id")
    branch_id: UUID = None
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
