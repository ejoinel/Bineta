#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Bineta import settings
from rest_framework import routers
from Bineta.views import login, home, register, createexam, reset_password, ExamListView, search_exam,\
    UserViewSet, PasswordReset, CreateUser, ExamViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'exams', ExamViewSet)


admin.autodiscover()

urlpatterns = [
    url( r'^api/v1/reset_password/', PasswordReset.as_view(), name="reset_password" ),
    url( r'^api/v1/register/', CreateUser.as_view(), name="register" ),
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^home', home),
    url(r'^login$', login),
    url(r'^register$', register),
    url(r'^createexam$', createexam),
    url(r'^exam_list$', ExamListView.as_view()),
    url(r'^account/reset_password', reset_password, name="reset_password"),
    url(r'^search$', search_exam),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'api/auth/', include('knox.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
