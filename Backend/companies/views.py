from rest_framework import generics, permissions
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly

class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadOnly]
