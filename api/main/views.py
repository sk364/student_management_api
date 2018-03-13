from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet

from .models import Course
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import StudentSerializer, CourseSerializer


class StudentViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdmin, )


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrReadOnly, )
