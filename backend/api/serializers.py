import re

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from api import models


class CategorySerializer(serializers.ModelSerializer):
    def validate_color(self, value):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
        if not match:
            raise serializers.ValidationError(
                "This field should contain HEX color representation")
        return value

    class Meta:
        model = models.Category
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)

    class Meta:
        model = models.Note
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        category = validated_data.pop('category', None)
        if category:
            name, color = category.get('name'), category.get('color')
            category_obj, created = models.Category.objects.get_or_create(
                user=user,
                name=name,
                color=color
            )
            category_obj.save()
            validated_data['category'] = category_obj
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        category = validated_data.pop('category', None)

        instance.body = validated_data['body']
        instance.save()

        if category and category.get('name'):
            name, color = category['name'], category['color']
            category_obj = models.Category.objects.create(
                user=user,
                name=name,
                color=color
            )
            instance.category = category_obj
            instance.save()
        else:
            if instance.category:
                instance.category.delete()

        return instance


class UserSerializer(serializers.ModelSerializer):
    total_notes = serializers.IntegerField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'total_notes',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('username'),
            password=attrs.get('password'),
        )

        if not user:
            message = ('Incorrect provided credentials')
            raise serializers.ValidationError(message, code='authentication')
        attrs['user'] = user

        return
