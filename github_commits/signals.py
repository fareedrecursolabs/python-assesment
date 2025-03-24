import json
import os
import redis
from django.db.models.signals import post_save
from django.dispatch import receiver
from github_commits.models import Commit


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@receiver(post_save, sender=Commit)
def send_commit_update(sender, instance, **kwargs):
    data = {
        "id": str(instance.id),
        "message": instance.message,
        "pushed_at": instance.pushed_at.isoformat(),
        "modified_files": instance.modified_files,
        "author_name": instance.author_name,
        "author_email": instance.author_email,
        "author_username": instance.author_username,
        "branch": instance.branch.name if instance.branch else None,
    }

    redis_client.publish(f"commits_{instance.branch_id}", json.dumps(data))
