from django.db import models
import uuid

class GithubRepo(models.Model):
  id = models.BigIntegerField(primary_key=True, editable=False)
  name = models.CharField(max_length=255)
  url = models.CharField(max_length=255)
  owner_name = models.CharField(max_length=255)
  owner_email = models.CharField(max_length=255)
  main_branch = models.CharField(max_length=255)

  def __str__(self):
    return self.name
