from rest_framework import serializers
from .models import PullRequest
from github_branches.serializer import BranchSerializer

class PullRequestSerializer(serializers.ModelSerializer):
  branch = BranchSerializer(read_only=True)
  class Meta:
    model = PullRequest
    fields = '__all__'
