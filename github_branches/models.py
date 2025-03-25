from django.db import models
from github_repos.models import GithubRepo
import uuid
# Create your models here.


class Branch(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=50)
  repo = models.ForeignKey(GithubRepo, on_delete=models.CASCADE, related_name="branches")

  def __str__(self):
        return f"{self.name} ({self.repo.name if self.repo else 'No Repo'})"
