from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import StudentViewSet, CourseViewSet


router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = router.urls
