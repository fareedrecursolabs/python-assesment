from django.db import models
import uuid
from github_branches.models import Branch

class Commit(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  message = models.CharField(max_length=255, blank=True, null=True)
  pushed_at = models.DateTimeField()
  modified_files = models.JSONField()
  author_name = models.CharField(max_length=255)
  author_email = models.CharField(max_length=255)
  author_username = models.CharField(max_length=255)
  branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="commits")

  def __str__(self):
    return f"{self.message} {self.branch.name}"
