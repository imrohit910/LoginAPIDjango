from rest_framework import serializers
from .models import MyApp
from django.contrib.auth.hashers import make_password

class MyAPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyApp
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password isn't returned in response

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
