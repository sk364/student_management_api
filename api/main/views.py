from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Course
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import StudentSerializer, CourseSerializer

REQUIRED_FIELDS_ABSENT_MSG = 'Required Field(s) absent.'
MIN_PASSWORD_LENGTH_MSG = 'Password should be at least 8 characters long.'
SUCCESS_REGISTRATION_MSG = 'Successfully Registered.'


class StudentViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdmin, )


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrReadOnly, )


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
        response = {}
        resp_status = None

        if username is None or password is None:
            response = {
                'success': False,
                'message': REQUIRED_FIELDS_ABSENT_MSG
            }
            resp_status = status.HTTP_400_BAD_REQUEST
        elif len(password) < 8:
            response = {
                'success': False,
                'message': MIN_PASSWORD_LENGTH_MSG
            }
        else:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            response = {
                'success': True,
                'message': SUCCESS_REGISTRATION_MSG,
                'redirect_url': '/login'
            }

        return Response(response, status=resp_status)
