from rest_framework import generics
from .serializer import RepoSerializer
from .models import GithubRepo

class RepoList(generics.ListAPIView):
  serializer_class = RepoSerializer
  queryset = GithubRepo.objects.all()



class RepoDetails(generics.RetrieveAPIView):
  serializer_class = RepoSerializer
  queryset = GithubRepo.objects.all()
