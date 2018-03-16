"""
Student Management api URL Configuration
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Student Management API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', schema_view),
    url(r'^login/$', obtain_jwt_token),
    url(r'^', include('main.urls')),
]

if settings.DEBUG != 'False':
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
