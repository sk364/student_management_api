from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Course


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active',
                  'is_superuser', 'is_staff', )


class CourseSerializer(serializers.ModelSerializer):
    users = StudentSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ('id', 'name', 'users', )
