# -*- coding: utf-8 -*-

from django.core import serializers
from django.contrib.auth import get_user_model
from django.contrib.messages import constants as message_constants
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

import FORM_PROPERTIES
import settings
import utils
from Bineta.models import User, DocumentFile, Exam
from Bineta.serializers import UserSerializer, PasswordResetSerializer, UserRegisterSerializer, ExamSerializer,\
    DocumentFileSerializer, ExamCreationSerializer

MESSAGE_TAGS = { message_constants.DEBUG: 'debug',
                 message_constants.INFO: 'info',
                 message_constants.SUCCESS: 'success',
                 message_constants.WARNING: 'warning',
                 message_constants.ERROR: 'danger', }


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of profile to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and request.method in ['POST']



class IsStaff(BasePermission):
    """
    Custom permission to only allow owners of profile to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user.is_staff



class IsActive(BasePermission):
    """
    Custom permission to only allow owners of profile to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user.is_active



class CreateUser( APIView ):

    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post( self, request ):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = User.objects.create_simple_user( email=serializer.data[ 'email' ],
                                                    password=serializer.data[ 'password' ],
                                                    last_name=serializer.data[ 'last_name' ],
                                                    first_name=serializer.data[ 'first_name' ],
                                                    gender=serializer.data[ 'gender' ],
                                                    birth_date=serializer.data[ 'birth_date' ],
                                                    school_id=serializer.data[ 'school' ] )

            if not user:
                return Response( status=status.HTTP_500_INTERNAL_SERVER_ERROR )

            return Response( status=status.HTTP_201_CREATED )
        else:
            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )



class CreateExam( APIView ):

    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAdminUser, IsStaff, IsActive ]

    serializer_class = ExamCreationSerializer

    def post( self, request ):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            vo_exam = Exam( level_id=serializer.data[ 'level' ], matter_id=serializer.data[ 'matter' ],
                            school_id=serializer.data[ 'school' ], year_exam=serializer.data[ 'year_exam' ],
                            exam_type=serializer.data[ 'exam_type' ], user_id=request.user.id )

            vo_exam.save()
            return Response( status=status.HTTP_201_CREATED, data=ExamSerializer(vo_exam).data )
        else:
            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )



class exam_add_photo( APIView ):

    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAdminUser ]

    serializer_class = DocumentFileSerializer
    parser_classes = (FormParser, MultiPartParser,)

    def post( self, request, exam_id=None ):
        if 'upload' in request.data:
            user_profile = self.get_object()
            user_profile.image.delete()

            upload = request.data['upload']

            user_profile.image.save(upload.name, upload)

            return Response(status=status.HTTP_201_CREATED, headers={'Location': user_profile.image.url})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ExamViewSet( viewsets.ModelViewSet ):


    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAuthenticated ]

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def list( self, request ):
        user = request.user
        if user.is_staff:
            queryset = Exam.objects.all()
        else:
            queryset = Exam.objects.filter( status=2 )
        serializer = ExamSerializer( queryset, many=True )
        return Response( serializer.data )

    def retrieve( self, request, pk=None ):
        user = request.user
        exam = get_object_or_404( User, pk=pk )

        if not user.is_staff and exam.status != 2:
            return Response( status=status.HTTP_401_UNAUTHORIZED )

        serializer = UserSerializer( exam )
        return Response( serializer.data )

    def create( self, request ):
        upload_files = request.FILES.get('files')
        if not upload_files:
            return Response(status=404)
        serializer = UserSerializer( None )
        return Response( serializer.data )


Exam_list = ExamViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


class DocumentfileSet( viewsets.ModelViewSet):

    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAuthenticated ]

    queryset = DocumentFile.objects.all()
    serializer_class = DocumentFileSerializer

    def list( self, request ):
        user = request.user
        if user.is_staff:
            queryset = Exam.objects.all()
        else:
            queryset = Exam.objects.filter( status=2 )
        serializer = ExamSerializer( queryset, many=True )
        return Response( serializer.data )

    def retrieve( self, request, pk=None ):
        user = request.user
        exam = get_object_or_404( User, pk=pk )

        if not user.is_staff and exam.status != 2:
            return Response( status=status.HTTP_401_UNAUTHORIZED )

        serializer = UserSerializer( exam )
        return Response( serializer.data )

    def create( self, request ):
        upload_files = request.FILES.get('files')
        if not upload_files:
            return Response(status=404)
        serializer = UserSerializer( None )
        return Response( serializer.data )



class UserViewSet( viewsets.ModelViewSet):

    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAuthenticated ]

    queryset = User.objects.all()
    serializer_class = UserSerializer


    def list( self, request ):
        user = request.user
        if user.is_staff:
            queryset = User.objects.all()
        else:
            queryset = [ user ]
        serializer = UserSerializer( queryset, many=True )
        return Response( serializer.data )

    def retrieve( self, request, pk=None ):
        user = request.user
        if user.is_staff:
            user = get_object_or_404( User, pk=pk )
        else:
            user = get_object_or_404( User, pk=pk )

            if user.id != pk:
                return Response( status=status.HTTP_401_UNAUTHORIZED )

        serializer = UserSerializer( user )
        return Response( serializer.data )

    def create(self, request):
        pass


    @detail_route(methods=['POST'], permission_classes=[ IsAdminUser ])
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        if 'upload' in request.data:
            user_profile = self.get_object()
            user_profile.image.delete()

            upload = request.data['upload']

            user_profile.image.save(upload.name, upload)

            return Response(status=status.HTTP_201_CREATED, headers={'Location': user_profile.thumbnail.url})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass


    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = get_object_or_404( User, pk=pk )
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    @detail_route(methods=['GET'], permission_classes=[ IsAdminUser ])
    def recent_users( self ):
        recent_users = User.objects.all().order( '-last_login' )

        page = self.paginate_queryset( recent_users )
        if page is not None:
            serializer = self.get_serializer( page, many=True )
            return self.get_paginated_response( serializer.data  )

        serializer = self.get_serializer( recent_users, many=True )
        return Response( serializer.data )



class PasswordReset(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post( self, request ):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']

            try:
                user = get_user_model().objects.get(email=email)
                if user and user.is_active:
                    subject = FORM_PROPERTIES.PASSWORD_RESET_SUBJECT.decode( 'utf8' )
                    subject = subject.replace( "site_name", "Bineta" )

                    new_password = utils.generate_code()
                    print new_password
                    user.set_password( new_password )

                    dict_values = { 'email': user.email, 'site_name': 'Bineta', 'user': user, 'password': new_password }
                    email_template_name = 'account/password_reset_email.html'

                    utils.send_email( to_email=user.email, from_email=settings.DEFAULT_FROM_EMAIL, context=dict_values,
                                      subject=subject, plain_body_template_name=email_template_name )

                    user.save( )
                    content = { 'detail': 'Password reset' }
                    return Response( content, status=status.HTTP_200_OK )

            except get_user_model().DoesNotExist:
                pass

            # Since this is AllowAny, don't give away error.
            content = { 'detail': 'Password reset not allowed.' }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )
