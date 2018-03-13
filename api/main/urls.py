from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import StudentViewSet, CourseViewSet, UserRegistrationAPIView


router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    url(r'register/$', UserRegistrationAPIView.as_view()),
] + router.urls
