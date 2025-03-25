from django.db import models
from github_repos.models import GithubRepo
from github_branches.models import Branch
import uuid

class PullRequest(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=50)
  body = models.TextField(null=True, blank=True)
  state = models.CharField(max_length=50)
  base_branch = models.CharField(max_length=50)
  head_branch = models.CharField(max_length=50)
  url = models.URLField(max_length=255)
  html_url = models.URLField(max_length=255)
  number = models.IntegerField(null=True, blank=True)
  commits = models.IntegerField(null=True, blank=True)
  additions = models.IntegerField(null=True, blank=True)
  deletions = models.IntegerField(null=True, blank=True)
  changed_files = models.IntegerField(null=True, blank=True)
  user = models.CharField(max_length=100)
  created_at = models.DateTimeField()
  updated_at = models.DateTimeField(blank=True, null=True)
  closed_at = models.DateTimeField(blank=True, null=True)
  merged_at = models.DateTimeField(blank=True, null=True)
  repo = models.ForeignKey(GithubRepo, on_delete=models.CASCADE, related_name="pull_requests")
  branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="pull_request_branch")

  def __str__(self):
    return f"{self.title} ({self.state})"
