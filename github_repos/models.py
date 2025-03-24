from django.db import models
import uuid

class GithubRepo(models.Model):
  id = models.BigIntegerField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=255, blank=True, null=True)
  url = models.CharField(max_length=255, blank=True, null=True)
  owner_name = models.CharField(max_length=255, blank=True, null=True)
  owner_email = models.CharField(max_length=255, blank=True, null=True)
  main_branch = models.CharField(max_length=255, blank=True, null=True)

  def __str__(self):
    return self.name
