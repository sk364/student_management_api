from django.contrib.auth.models import User

from rest_framework import serializers

from .constants import MAX_STUDENTS_IN_COURSE
from .models import Course


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active',
                  'is_superuser', 'is_staff', )


class CourseSerializer(serializers.ModelSerializer):
    users = StudentSerializer(read_only=True, many=True)

    def get_is_available(self, obj):
        return obj.users.count() < MAX_STUDENTS_IN_COURSE

    is_available = serializers.SerializerMethodField(read_only=True)

    def get_is_enrolled(self, obj):
        user = self.context['user']
        return obj.users.filter(id=user.id).count() == 1

    is_enrolled = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'users', 'is_available', 'is_available', 'is_enrolled', )
