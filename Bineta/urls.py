#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Bineta import settings
from rest_framework import routers
from Bineta.views import login, home, register, reset_password, search_exam
from Bineta.bineta_api import UserViewSet, PasswordReset, CreateUser, ExamViewSet, CreateExam, Exam_list, exam_add_photo

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'exams', ExamViewSet)


admin.autodiscover()

urlpatterns = [
    url( r'^api/v1/reset_password/', PasswordReset.as_view(), name="reset_password" ),
    url( r'^api/v1/register/', CreateUser.as_view(), name="register" ),
    url( r'^api/v1/exams/', Exam_list, name="exams" ),
    url( r'^api/v1/create_exam/', CreateExam.as_view(), name="create_exam" ),
    url( r'^api/v1/exam_add_photo/(?P<exam_id>\d+)/$', exam_add_photo.as_view(), name="exam_add_photo" ),
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^home', home),
    url(r'^login$', login),
    url(r'^register$', register),
    url(r'^account/reset_password', reset_password, name="reset_password"),
    url(r'^search$', search_exam),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'api/auth/', include('knox.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
