from rest_framework import serializers
from rest_framework.authentication import authenticate

from .models import CustomUser


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if not password or not confirm_password:
            raise serializers.ValidationError("Введите пароль и подтверждение пароля")

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают")

        attrs.pop("confirm_password")
        return attrs

    def validate_email(self, value):
        cheak_email = CustomUser.objects.filter(email=value).exists()
        if cheak_email:
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже существует"
            )
        return value

    def update(self, instance, data):
        instance.username = data.get("username", instance.title)
        instance.email = data.get("email", instance.email)
        instance.password = data.get("password", instance.password)

        instance.save()
        return instance

    def create(self, data):
        return CustomUser.objects.create_user(**data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Вы не ввели username")
        cheak_username = CustomUser.objects.filter(username=value).exists()
        if not cheak_username:
            raise serializers.ValidationError("Такого пользователя не существует")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Вы не ввели пароль")
        return value

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if getattr(user, "status", None) == "block":
            raise serializers.ValidationError("Ваш аккаунт заблокирован")

        attrs["user"] = user

        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
        )
