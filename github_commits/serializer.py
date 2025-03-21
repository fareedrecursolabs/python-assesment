from rest_framework import serializers
from .models import Commit
from github_repos.serializer import RepoSerializer

class CommitsSerializer(serializers.ModelSerializer):
  repo_name = RepoSerializer(read_only=True)
  class Meta:
    model = Commit
    fields = '__all__'
