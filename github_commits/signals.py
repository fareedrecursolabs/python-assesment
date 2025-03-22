import json
import redis
from django.db.models.signals import post_save
from django.dispatch import receiver
from github_commits.models import Commit

# Initialize Redis client
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

@receiver(post_save, sender=Commit)
def send_commit_update(sender, instance, **kwargs):
    """
    Triggered when a new commit is saved.
    Publishes commit data to a Redis channel.
    """
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

    # Publish commit data to a Redis channel
    redis_client.publish(f"commits_{instance.branch_id}", json.dumps(data))
