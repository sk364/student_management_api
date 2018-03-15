from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .constants import (MAX_STUDENTS_IN_COURSE, MIN_PASSWORD_LENGTH_MSG,
                        REQUIRED_FIELDS_ABSENT_MSG, PASSWORDS_DO_NOT_MATCH_MSG,
                        SUCCESS_REGISTRATION_MSG, )
from .models import Course
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import StudentSerializer, CourseSerializer


class StudentViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
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
        user = request.data.get('user_id') or request.user

        response = {'success': False}
        resp_status = status.HTTP_400_BAD_REQUEST

        try:
            course = Course.objects.get(pk=pk)
            course.users.remove(user)
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
        confirm_password = request.data.get('confirm_password')
        response = {'success': False}
        resp_status = status.HTTP_400_BAD_REQUEST

        if username is None or password is None:
            response['message'] = REQUIRED_FIELDS_ABSENT_MSG
        elif len(password) < 8 or len(confirm_password) < 8:
            response['message'] = MIN_PASSWORD_LENGTH_MSG
        elif password != confirm_password:
            response['message'] = PASSWORDS_DO_NOT_MATCH_MSG
        else:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            response = {
                'success': True,
                'message': SUCCESS_REGISTRATION_MSG,
                'redirect_url': '/login'
            }
            resp_status = status.HTTP_201_CREATED

        return Response(response, status=resp_status)


class ChangePasswordAPIView(APIView):
    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        response = {'success': False}
        resp_status = status.HTTP_400_BAD_REQUEST

        if current_password is None or new_password is None or confirm_password is None:
            response['message'] = REQUIRED_FIELDS_ABSENT_MSG
        else:
            is_current_password_valid = user.check_password(current_password)
            if is_current_password_valid is False:
                response['message'] = 'Incorrect Current Password.'
            elif len(new_password) < 8 or len(confirm_password) < 8:
                response['message'] = 'Passwords should be atleast 8 characters long.'
            elif new_password != confirm_password:
                response['message'] = PASSWORDS_DO_NOT_MATCH_MSG
            else:
                user.set_password(new_password)
                user.save()
                response = {
                    'success': True,
                    'message': 'Password Updated Successfully.'
                }
                resp_status = status.HTTP_200_OK

        return Response(response, status=resp_status)
