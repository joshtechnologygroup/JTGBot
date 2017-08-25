# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt$', lambda r: HttpResponse('User-agent: *\nDisallow: /msg', content_type='text/plain')),
]
