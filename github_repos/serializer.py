from rest_framework import serializers
from .models import GithubRepo

class RepoSerializer(serializers.ModelSerializer):
  class Meta:
    model = GithubRepo
    fields = '__all__'
