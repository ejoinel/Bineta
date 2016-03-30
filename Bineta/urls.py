#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Bineta import settings
from rest_framework import routers
from Bineta.views import login, home, register, createexam, reset_password, ExamListView, search_exam, UserViewSet

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

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
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
