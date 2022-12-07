from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from vincent.models import User


class UserTokenObtainSerializer(TokenObtainPairSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=150)

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['id'] = self.user.id

        return data


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'created_at', 'updated_at', 
            'username', 'email',
            'first_name', 'last_name',
        )