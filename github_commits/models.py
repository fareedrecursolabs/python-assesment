from django.db import models
import uuid
from github_branches.models import Branch

class Commit(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  message = models.CharField(max_length=255, blank=True, null=True)
  pushed_at = models.DateTimeField(blank=True, null=True)
  modified_files = models.JSONField(blank=True, null=True)
  author_name = models.CharField(max_length=255, blank=True, null=True)
  author_email = models.CharField(max_length=255, blank=True, null=True)
  author_username = models.CharField(max_length=255, blank=True, null=True)
  branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="commits", blank=True, null=True)

  def __str__(self):
    return self.message
