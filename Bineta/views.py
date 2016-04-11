# -*- coding: utf-8 -*-

from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as super_login
from django.contrib.auth import logout as super_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.messages import constants as message_constants
from django.core.mail import send_mail
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.views.generic import ListView
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import FORM_PROPERTIES
import models
import settings
import utils
from Bineta.forms import LoginForm, UserForm, CreateExamForm, AccountResetPassword
from Bineta.models import User, DocumentFile, Exam
from Bineta.serializers import UserSerializer, PasswordResetSerializer
from Bineta.settings import DEFAULT_FROM_EMAIL

MESSAGE_TAGS = { message_constants.DEBUG: 'debug',
                 message_constants.INFO: 'info',
                 message_constants.SUCCESS: 'success',
                 message_constants.WARNING: 'warning',
                 message_constants.ERROR: 'danger', }



class UserViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        user = request.user
        if user.is_staff:
            queryset = User.objects.all()
        else:
            queryset = [ user ]
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user
        if user.is_staff:
            user = get_object_or_404(User, pk=pk)
        else:
            user = get_object_or_404(User, pk=pk)

            if user.id != pk:
                return Response( status=status.HTTP_401_UNAUTHORIZED )

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass


    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def recent_users(self, request):
        recent_users = User.objects.all().order('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


class PasswordReset(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post( self, request, format=None ):
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



def get_logged_user_from_request( request ):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session[ 'logged_user_id' ]
        users = User.objects.get( id=logged_user_id )
        if not users:
            return None
        if isinstance( users, list ):
            return users[ 0 ]
        else:
            return users
    else:
        return None


def search_exam( request ):
    vos_exam = []
    if request.method == 'POST':
        search_text = request.POST["search_text"]
        if len( search_text ) >= 2:
            search_array = search_text.split(' ')
            vos_exam = Exam.objects.filter(reduce(lambda x, y: x | y, [Q(name__contains=word) for word in search_array]))

    return render_to_response( "ajax_search.html", {'vos_exam': vos_exam} )



# @login_required(login_url='/login')
def home( request ):
    logged_user = get_logged_user_from_request( request=request )
    if logged_user:
        return render_to_response( 'home.html', { 'current_date_time': datetime.now( ), 'logged_user': logged_user } )
    else:
        return HttpResponseRedirect( '/login' )



def logout( request ):
    super_logout( request )
    return HttpResponseRedirect( '/login' )


# @login_required(login_url='/login')
class ExamListView( ListView ):

    model = models.Exam
    template_name = 'exam_list.html'
    context_object_name = "vos_exam"
    paginate_by = 2

    def get_queryset(self):
        return Exam.objects.order_by('-creation_date')[:3]

    def get_context_data(self, **kwargs):
        context = super(ExamListView, self).get_context_data(**kwargs)
        vos_exam = Exam.objects.order_by('-creation_date')[:3]
        for vo_exam in vos_exam:
            vo_image = DocumentFile.objects.filter( document_id=vo_exam.document_ptr_id)[0]
            vo_exam.image = vo_image.image.url if vo_image else None
            vo_exam.display_title = vo_exam.level.name
            if vo_exam.level.sub_category:
                vo_exam.display_title += "({})".format( vo_exam.level.sub_category )
            vo_exam.display_title += " - {}".format( vo_exam.matter.name)
            display_type_exam = "" if vo_exam.mock_exam else ""
            vo_exam.diplay_info = "{}({}) - {}".format( vo_exam.school.name, vo_exam.year_exam, display_type_exam )

        paginator = Paginator(vos_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            vos_exam = paginator.page(page)
        except PageNotAnInteger:
            vos_exam = paginator.page(1)
        except EmptyPage:
            vos_exam = paginator.page(paginator.num_pages)

        context['vos_exam'] = vos_exam
        return context



def reset_password( request ):
    # Test si le fomulaire a été envoyé
    if request.method == "POST":
        form = AccountResetPassword( request.POST )
        context = { 'form': form }

        if form.is_valid( ):
            email = form.cleaned_data[ 'email' ]
            users = User.objects.filter( email=email )

            if users:
                # the password verified for the user
                user = users[ 0 ]
                if user.is_active:
                    subject = FORM_PROPERTIES.PASSWORD_RESET_SUBJECT.decode( 'utf8' )
                    subject = subject.replace( "site_name", "Bineta" )
                    new_password = User.objects.make_random_password( length=6 )
                    print new_password
                    user.set_password( new_password )
                    dict_values = { 'email': user.email, 'site_name': 'MBacho', 'user': user, 'password': new_password }
                    email_template_name = 'account/password_reset_email.html'
                    email = loader.render_to_string( email_template_name, dict_values )
                    if send_mail( subject, email, DEFAULT_FROM_EMAIL, [ user.email ], fail_silently=False ):
                        msg = FORM_PROPERTIES.PASSWORD_RESET.decode( 'utf8' )
                        msg = msg.replace( "user", user.email )
                        messages.add_message( request, messages.SUCCESS, msg )
                        user.save( )
                        return HttpResponseRedirect( '/login' )
                    else:
                        msg = FORM_PROPERTIES.PASSWORD_NOT_SENT.decode( 'utf8' )
                        messages.add_message( request, messages.ERROR, msg )
                        return render_to_response( template_name='account/resetpassword.html', context=context,
                                                   context_instance=RequestContext( request ) )
                else:
                    msg = FORM_PROPERTIES.FORM_LOGIN_NOT_ACTIVE.decode( 'utf8' )
                    messages.add_message( request, messages.ERROR, msg )
                    return render_to_response( template_name='account/resetpassword.html', context=context,
                                               context_instance=RequestContext( request ) )
            else:
                msg = FORM_PROPERTIES.FORM_USER_NOT_FOUND.decode( 'utf8' )
                messages.add_message( request, messages.ERROR, msg )
                return render_to_response( template_name='account/resetpassword.html', context=context,
                                           context_instance=RequestContext( request ) )
        else:
            context = { 'form': form }
            return render_to_response( template_name='account/resetpassword.html', context=context,
                                       context_instance=RequestContext( request ) )
    else:
        form = AccountResetPassword( )
        context = { 'form': form }
        return render_to_response( template_name='account/resetpassword.html', context=context,
                                   context_instance=RequestContext( request ) )



def login( request ):
    # Test si le fomulaire a été envoyé
    if request.method == "POST":
        form = LoginForm( request.POST )
        context = { 'form': form }

        if form.is_valid( ):
            password = form.cleaned_data[ 'password' ]
            email = form.cleaned_data[ 'email' ]
            user = authenticate( email=email, password=password )

            if user:
                # the password verified for the user
                if user.is_active:
                    super_login( request, user )
                    msg = FORM_PROPERTIES.WELCOME_MSG.decode( 'utf8' )
                    msg = msg.replace( "user", user.nickname )
                    messages.add_message( request, messages.SUCCESS, msg )
                    request.session[ 'logged_user_id' ] = user.id
                    return HttpResponseRedirect( '/home' )
                else:
                    messages.add_message( request, messages.WARNING,
                                          FORM_PROPERTIES.FORM_LOGIN_NOT_ACTIVE )
                    return render_to_response( template_name='login.html', context=context,
                                               context_instance=RequestContext( request ) )
            else:
                msg = FORM_PROPERTIES.FORM_LOGIN_FAILED

                messages.add_message( request, messages.WARNING, msg )
                return render_to_response( template_name='login.html', context=context,
                                           context_instance=RequestContext( request ) )
        else:
            msg = FORM_PROPERTIES.FORM_LOGIN_FAILED
            messages.add_message( request, messages.WARNING, msg )
            return render_to_response( template_name='login.html', context=context,
                                       context_instance=RequestContext( request ) )
    else:
        form = LoginForm( )
        context = { 'form': form }
        return render_to_response( template_name='login.html', context=context,
                                   context_instance=RequestContext( request ) )



@login_required( login_url='/login' )
def createexam( request ):
    # Creation du formulaire + upload des images
    doc_form = CreateExamForm( auto_id=True )

    # Récupération du formulaire géré par le mécanisme formset
    # formset = sortedfilesform()

    if request.method == "POST":

        doc_form = CreateExamForm( request.POST, request.FILES )

        if doc_form.is_valid( ):
            new_doc = Exam( level=doc_form.cleaned_data[ 'level' ], matter=doc_form.cleaned_data[ 'matter' ],
                            school=doc_form.cleaned_data[ 'school' ], year_exam=doc_form.cleaned_data[ 'year_exam' ],
                            mock_exam=doc_form.cleaned_data[ 'mock_exam' ] )
            new_doc.user = request.user
            new_doc.user_id = request.user.id
            new_doc.save( )
            document_files = doc_form.cleaned_data[ 'first_files' ] + doc_form.cleaned_data[ 'second_files' ]
            for i, one_file in enumerate( document_files ):
                vo_file = DocumentFile( description="Page {}".format( i + 1 ), image=one_file, document=new_doc )
                vo_file.temp_id = format( i + 1 )
                vo_file.save( )
            return HttpResponseRedirect( '/login' )
        else:
            context = { 'doc_form': doc_form, }
            return render( request, 'createexam.html', context )


    else:
        context = { 'doc_form': doc_form, }
        return render( request, 'createexam.html', context )



def register( request ):
    if request.method == "POST":
        form = UserForm( request.POST )
        form_values = { 'form': form }
        error_form = False

        if form.is_valid( ):
            if 'nickname' in form.cleaned_data:
                nickname = form.cleaned_data[ 'nickname' ]
            else:
                nickname = form.cleaned_data[ 'email' ].split( "@" )[ 0 ]
            mail = form.cleaned_data[ 'email' ]

            if form.cleaned_data[ 'password1' ] != form.cleaned_data[ 'password2' ]:
                error_form = True
                messages.add_message( request, messages.WARNING,
                                      FORM_PROPERTIES.FORM_MSG_PASSWORD_NO_MATCHING )

            # les speudo et mail sont uniques
            nb_nickname = len( User.objects.filter( nickname=nickname ) )
            if nb_nickname > 0:
                nickname = "{}_{}".format( nickname, nb_nickname + 1 )

            if len( User.objects.filter( email=mail ) ) > 0:
                error_form = True
                messages.add_message( request, messages.WARNING,
                                      FORM_PROPERTIES.FORM_MAIL_USED )

            if error_form:
                return render_to_response( 'register.html', form_values,
                                           context_instance=RequestContext( request ) )

            msg = FORM_PROPERTIES.FORM_MSG_ACCOUNT_CREATED.decode( 'utf8' )
            msg = msg.replace( "name", nickname )

            stored_user = form.save( commit=False )
            stored_user.password = make_password( form.cleaned_data[ 'password1' ] )
            stored_user.nickname = nickname
            stored_user.save( )
            messages.add_message( request, messages.SUCCESS, msg )

            return HttpResponseRedirect( '/login' )
        else:
            messages.add_message( request, messages.ERROR,
                                  FORM_PROPERTIES.FORM_MSG_ACCOUNT_ERROR )

            return render_to_response( 'register.html', form_values, context_instance=RequestContext( request ) )

    else:
        form = UserForm( )
        form_values = { 'form': form }
        return render_to_response( 'register.html', form_values, context_instance=RequestContext( request ) )
