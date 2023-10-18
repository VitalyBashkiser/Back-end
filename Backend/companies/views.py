from rest_framework import viewsets, permissions, status
from .models import Company
from .serializers import CompanySerializer
from main.pagination import CustomPageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Company.objects.all()
        else:
            return Company.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.owner:
            serializer.save()
        else:
            raise PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user == instance.owner:
            instance.delete()
        else:
            raise PermissionDenied()


@api_view(['POST'])
def toggle_company_visibility(request, pk):
    try:
        company = Company.objects.get(pk=pk)
        company.is_visible = not company.is_visible
        company.save()
        return Response(status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)