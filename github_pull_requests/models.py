from django.db import models
from github_repos.models import GithubRepo
import uuid

class PullRequest(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=50, null=True, blank=True)
  state = models.CharField(max_length=50, null=True, blank=True)
  url = models.CharField(max_length=255, null=True, blank=True)
  user = models.CharField(max_length=100, null=True, blank=True)
  created_at = models.DateTimeField(blank=True, null=True)
  repo = models.ForeignKey(GithubRepo, on_delete=models.CASCADE, related_name="pull_requests", blank=True, null=True)

  def __str__(self):
    return f"{self.title} ({self.state})"
