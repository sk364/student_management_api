from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .constants import (MAX_STUDENTS_IN_COURSE, MIN_PASSWORD_LENGTH_MSG,
                        REQUIRED_FIELDS_ABSENT_MSG, SUCCESS_REGISTRATION_MSG, )
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

    def get_serializer_context(self):
        return {'user': self.request.user}

    @detail_route(methods=['put'], permission_classes=(IsAuthenticated, ))
    def enroll(self, request, pk):
        response = {'success': False}
        resp_status = status.HTTP_400_BAD_REQUEST

        try:
            course = Course.objects.get(pk=pk)

            if course.users.count() < MAX_STUDENTS_IN_COURSE:
                course.users.add(request.user)
                users = [user.id for user in course.users.all()]

                response = {
                    'success': True,
                    'users': users,
                    'is_available': len(users) < MAX_STUDENTS_IN_COURSE,
                }
                resp_status = status.HTTP_201_CREATED
            else:
                response['message'] = 'Course full'
        except Course.DoesNotExist:
            response['message'] = 'Course with id {} does not exist.'.format(pk)

        return Response(response, status=resp_status)

    @detail_route(methods=['put'], permission_classes=(IsAuthenticated, ))
    def leave(self, request, pk):
        response = {'success': False}
        resp_status = status.HTTP_400_BAD_REQUEST

        try:
            course = Course.objects.get(pk=pk)
            course.users.remove(request.user)
            users = [user.id for user in course.users.all()]

            response = {
                'success': True,
                'users': users,
            }
            resp_status = status.HTTP_200_OK
        except Course.DoesNotExist:
            response['message'] = 'Course with id {} does not exist.'.format(pk)

        return Response(response, status=resp_status)


class UserRegistrationAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        API View that registers users in the app.

        :form: `username` Username string

        :form: `password` Password string

        :response: `200` Successfully Registered

        :response: `400` Required fields absent

        :response: `400` Password length is less than 8
        """

        username = request.data.get('username')
        password = request.data.get('password')
        response = {'success': False}
        resp_status = status.HTTP_400_BAD_REQUEST

        if username is None or password is None:
            response['message'] = REQUIRED_FIELDS_ABSENT_MSG
        elif len(password) < 8:
            response['message'] = MIN_PASSWORD_LENGTH_MSG
        else:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            response = {
                'success': True,
                'message': SUCCESS_REGISTRATION_MSG,
                'redirect_url': '/login'
            }
            status = status.HTTP_201_CREATED

        return Response(response, status=resp_status)
