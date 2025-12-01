from rest_framework import serializers
from rest_framework.authentication import authenticate
import re

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
        check_username = CustomUser.objects.filter(username=value).exists()
        if not check_username:
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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            'password'
            'role',
            'status'
        )
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = CustomUser(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

        def validate_username(self, value):
            if len(value) < 8:
                raise serializers.ValidationError('Введите username больше 8 символов')
            raise value

        def validate_password(self, value):
            VALID_SPEC_SYMB = r'!@#$%^&*_+\-,./?:;"\'~`|\\'
            VALID_UPPERCASE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if len(value) < 8:
                raise serializers.ValidationError('Введите пароль больше 8 символов')
            has_special_char = any(char in VALID_SPEC_SYMB for char in value)
            if not has_special_char:
                raise serializers.ValidationError("Введите хотя-бы 1 спец символ")
            has_uppercase_letter = any(char in VALID_UPPERCASE_LETTERS for char in value)
            if not has_uppercase_letter:
                raise serializers.ValidationError("Введите хотя-бы одну заглавную букву")
            return value