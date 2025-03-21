from django.shortcuts import render
from rest_framework import generics
from .models import Branch
from .serializer import BranchSerializer

# Create your views here.
class BranchList(generics.ListAPIView):
  serializer_class = BranchSerializer
  queryset = Branch.objects.all()



class BranchDetails(generics.RetrieveAPIView):
  serializer_class = BranchSerializer
  queryset = Branch.objects.all()
