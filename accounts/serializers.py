from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from rest_framework.validators import UniqueValidator

from accounts.models import User
from trainees.models import Trainee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "firstname", "lastname", "email"]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "firstname", "lastname", "email", "password", "password_confirm"]
        extra_kwargs = {
            'firstname': {'required': True},
        }

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords don't match"})

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password')
            validated_data.pop('password_confirm')

            user = self.Meta.model(**validated_data)
            user.set_password(password)
            user.save()

            Trainee.objects.create(user=user)

        return user
