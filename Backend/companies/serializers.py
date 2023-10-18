from rest_framework import serializers
from .models import Company
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'is_visible', 'owner']

    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )


    def create(self, validated_data):
        owner = validated_data.pop('owner', None)
        company = Company.objects.create(owner=owner, **validated_data)
        return company