"""pyteams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from rest_api.views import (RESTApi, ApiInfo)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RESTApi.as_view(), name='rest_api'),
    url(r'(?P<handle>[-\w]+)/(?P<method>[-\w]+)/(?P<id>[-\w]+)/$', RESTApi.as_view(), name='handler'),
    url(r'^info', ApiInfo.as_view(), name='api_info')
]
