from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)

    email = serializers.EmailField(max_length=127)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(required=False)
    is_employee = serializers.BooleanField(default=False)

    is_superuser = serializers.BooleanField(default=False)

    password = serializers.CharField(write_only=True)

    def validate_email(self, v):
        if User.objects.filter(email=v).exists():
            raise ValidationError("email already registered.")
        return v

    def validate_username(self, v):
        if User.objects.filter(username=v).exists():
            raise ValidationError("username already taken.")
        return v

    def create(self, validated_data):
        if validated_data["is_superuser"] is False and validated_data["is_employee"] is False:
            user = User.objects.create_user(**validated_data) 
        else:
            validated_data["is_superuser"] = True
            user = User.objects.create_superuser(**validated_data)
        return user

    def update(self, instance: User, validated_data: dict):
        for k, v in validated_data.items():
            if k=='password':
                instance.set_password(v)
            else:
                setattr(instance, k, v)
        instance.save()
        return instance
