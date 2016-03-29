from tastypie.resources import ModelResource
from Bineta.models import User, Exam
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication

class UserResource( ModelResource ):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'User'
        excludes = ['id', 'email', 'password', 'is_staff', 'is_superuser']
        list_allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class ExamResource( ModelResource ):
    class Meta:
        queryset = Exam.objects.all()
        resource_name = 'Exam'
        list_allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
