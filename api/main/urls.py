from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import StudentViewSet, CourseViewSet, UserRegistrationAPIView, ChangePasswordAPIView


router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    url(r'signup/$', UserRegistrationAPIView.as_view(), name="signup"),
    url(r'change-password/$', ChangePasswordAPIView.as_view(), name="change-password"),
] + router.urls
