#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Bineta import settings
from rest_framework import routers
from Bineta.views import login, home, register, createexam, reset_password, ExamListView, search_exam, UserListAPIView, user_get_all, user_get_from_id

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.

urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^home', home),
    url(r'^login$', login),
    url(r'^register$', register),
    url(r'^createexam$', createexam),
    url(r'^exam_list$', ExamListView.as_view()),
    #url(r'^exam_detail/(?P<pk>\d+)/', views.exam_detail, name='person_detail'),
    url(r'^account/reset_password', reset_password, name="reset_password"),
    url(r'^search$', search_exam ),

    url(r'^auth-token/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth-token-refresh/$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^auth-token-verify/$', 'rest_framework_jwt.views.verify_jwt_token'),
    # api
    url(r'api/v1/users/', UserListAPIView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
