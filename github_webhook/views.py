import hashlib
import hmac
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_github_webhook
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


SECRET_TOKEN = os.getenv("GITHUB_WEBHOOK_SECRET")


def custom_ratelimit_view(request, exception):
    """Custom view to handle rate limit exceeded errors"""
    return JsonResponse({"error": "Rate limit exceeded"}, status=429)


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
@ratelimit(key='ip', rate='5/m', method='POST' , block=True)
@api_view(["POST"])
@permission_classes([AllowAny])
def github_webhook(request):
    """Django view for GitHub Webhook, triggers Celery task"""

    if not verify_github_signature(request):
        return Response({"error": "Unauthorized"}, status=401)

    payload = request.data.get('payload', None)

    if payload and isinstance(payload, list) and len(payload) > 0:
        data_to_process = payload[0]
    else:
        # If payload is not in the expected format, pass the entire request data
        data_to_process = request.data

    # Trigger Celery task asynchronously
    process_github_webhook.delay(data_to_process)

    return Response({"message": "Webhook received, processing in background"}, status=202)
