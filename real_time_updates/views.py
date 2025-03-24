import os
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
import asyncio
import sys
import redis.asyncio as redis  # Use asyncio-compatible Redis client
from rest_framework.renderers import BaseRenderer



async def event_stream(branch_id):
    print(f"✅ SSE Connected. Listening to commits_{branch_id}")
    sys.stdout.flush()

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"commits_{branch_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield f"data: {message['data']}\n\n"
            await asyncio.sleep(0.1)  # Small delay to prevent CPU overuse
    except asyncio.CancelledError:
        print("❌ SSE Connection Closed")
    finally:
        await pubsub.unsubscribe(f"commits_{branch_id}")
        await pubsub.close()
        await redis_client.close()


class SSERenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "sse"
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data

@api_view(["GET"])
@renderer_classes([SSERenderer])  # Override DRF rendering
@permission_classes([AllowAny])
def sse_stream(request, branch_id):
    response = StreamingHttpResponse(
        event_stream(branch_id), content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"  # Helps with streaming in Nginx setups

    return response
