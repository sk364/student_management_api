from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from .models import Course

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CourseTests(APITestCase):
    def setUp(self):
        User.objects.create(username='/dev/random', is_superuser=True)
        User.objects.create(username='noobyIsland')
        Course.objects.create(name='Advanced Data Structures')
        Course.objects.create(name='Introduction to AI')
        Course.objects.create(name='Philosophy of Coding')

    def set_credentials(self, username):
        if username is None:
            self.client.credentials()
            return

        user = User.objects.get(username=username)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def _test_get_courses(self):
        url = reverse('course-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0]['name'], 'Advanced Data Structures')
        self.assertEqual(response.data[1]['name'], 'Introduction to AI')
        self.assertEqual(response.data[2]['name'], 'Philosophy of Coding')

    def test_get_courses(self):
        """
        Tests course listing
        """

        self.set_credentials('/dev/random')
        self._test_get_courses()

        self.set_credentials('noobyIsland')
        self._test_get_courses()

        self.set_credentials(None)
        url = reverse('course-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_enrollment(self):
        """
        Tests course enrolling
        """

        username = 'noobyIsland'
        self.set_credentials(username)

        test_course_id = 1
        user = User.objects.get(username=username)
        admin_user = User.objects.get(username='/dev/random')
        course = Course.objects.get(id=test_course_id)
        url = reverse('course-enroll', kwargs={'pk': course.id})
        data = {'user_ids': [1]}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(course.users.count(), 1)
        self.assertEqual(course.users.get(username='/dev/random'), admin_user)

        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(course.users.count(), 2)
        self.assertEqual(course.users.get(username=username), user)

        # check for unauthenticated user
        self.set_credentials(None)
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(course.users.count(), 2)
