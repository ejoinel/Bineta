#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Bineta import settings
from rest_framework_expiring_authtoken import views
from rest_framework import routers
from Bineta.views import login, home, register, createexam, reset_password, ExamListView, search_exam, ProductViewSet

router = routers.DefaultRouter()
router.register(r'users', ProductViewSet)

admin.autodiscover()

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
    url(r'^search$', search_exam),
    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_expiring_auth_token)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
