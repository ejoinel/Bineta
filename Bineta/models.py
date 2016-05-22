# -*- coding: utf-8 -*-

# import DATABASE_CONF
import os
import utils
from Bineta import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token

FILE_TYPE = (
    (1, 'image'),
    (2, 'pdf'),
    (3, 'video'),
)

DOCUMENT_STATUS = (
    (1, 'new'),
    (2, 'cleared'),
    (3, 'deleted'),
)

EXAM_YEAR_CHOICES = (
    (2016, '2016'),
    (2015, '2015'),
    (2014, '2014'),
    (2013, '2013'),
    (2012, '2012'),
    (2011, '2011'),
)


def upload_function( instance, filename ):

    ext = filename.split( '.' )[-1]
    filename = "{}_{}.{}".format( instance.document.id, instance.temp_id, ext )
    document_path = "{}/{}/{}/{}/{}/{}"
    doc_level = "{}{}".format( instance.document.level.name, instance.document.level.sub_category )

    document_path = document_path.format( instance.document.document_type, instance.document.school.name, doc_level,
                                          instance.document.matter.name, instance.document.year_exam,
                                          instance.document.id )

    parsed_document_path = "{}/{}".format( utils.remove_accents_spaces( document_path ), filename )

    return os.path.join( '{}'.format( parsed_document_path ) )



def upload_thumbnail( instance, filename ):

    filename = "{}.{}".format( instance.email, "png" )
    document_path = "ImagesProfile/{}".format( filename )

    return os.path.join( document_path )



def upload_document_thumbnail( instance, filename ):

    filename = "{}.{}".format( instance.id, "png" )
    document_path = "ImagesDocument/{}".format( filename )

    return os.path.join( document_path )



class ClassLevel( models.Model ):
    class Meta:
        db_table = 'ClassLevel'

    name = models.CharField( max_length=30 )
    sub_category = models.CharField( max_length=30 )

    def __unicode__( self ):
        if self.sub_category:
            return self.name + "(" + self.sub_category + ")"
        else:
            return self.name



class School( models.Model ):
    class Meta:
        db_table = 'School'

    name = models.CharField( max_length=100 )

    def __unicode__( self ):
        return self.name



class Subscription( models.Model ):
    class Meta:
        db_table = 'Subscription'

    name = models.CharField( max_length=30 )
    is_monthly = models.BooleanField( 'monthly', default=True )
    is_annual = models.BooleanField( 'annual', default=False )
    creation_date = models.DateTimeField( 'creation_date', default=timezone.now )
    modification_date = models.DateTimeField( 'modification_date', default=timezone.now )
    deletion_date = models.DateTimeField( 'deletion_date', default=None, blank=True, null=True )

    def __unicode__( self ):
        return self.name



class ClassTopic( models.Model ):
    class Meta:
        db_table = 'ClassTopic'

    name = models.CharField( max_length=30 )

    def __unicode__( self ):
        return self.name



class UserManager( BaseUserManager ):

    def create_user( self, email, password, **kwargs ):
        user = self.model( email=self.normalize_email( email ), is_active=True, **kwargs )
        user.set_password( password )
        user.save( )
        return user

    def create_simple_user( self, email, password, last_name, first_name, gender='M', birth_date=None, school_id=None,
                            **kwargs ):

        image_profile = None

        user = self.model( email=self.normalize_email( email ), is_active=True, is_admin=False,
                           last_name=last_name, first_name=first_name, gender=gender, birth_date=birth_date,
                           school_id=school_id, is_staff=False, **kwargs )

        user.identifier = utils.get_user_identifier()

        if user.gender == "M":
            image_profile = utils.get_random_image( settings.MEDIA_IMAGE_PROFILE_MEN )

        elif user.gender == "F":
            image_profile = utils.get_random_image( settings.MEDIA_IMAGE_PROFILE_WOMEN )

        if image_profile:
            user.thumbnail = utils.copy_file_in_media( src_file=image_profile )
        user.set_password( password )
        user.save()
        return user

    def create_superuser( self, email, password, **kwargs ):
        user = self.model( email=email, is_staff=True, is_superuser=True, is_active=True, **kwargs )
        user.set_password( password )
        user.save( )
        return user



class User( AbstractBaseUser, PermissionsMixin ):
    USERNAME_FIELD = 'email'

    GENDER_UNKNOWN = 'U'
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, _('unknown')),
        (GENDER_MALE, _('male')),
        (GENDER_FEMALE, _('female')),
    )

    class Meta:
        app_label = 'Bineta'
        db_table = "User"

    slug = models.SlugField( max_length=100 )
    nickname = models.SlugField( max_length=20, null=True, blank=True )
    first_name = models.CharField( max_length=30, default=None, null=True )
    last_name = models.CharField( max_length=30, default=None, null=True )
    school = models.ForeignKey( School, null=True, blank=True, default=None )
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    birth_date = models.DateField( default=None, blank=True, null=True )
    email = models.EmailField( 'email address', unique=True, max_length=254, db_index=True )
    identifier = models.CharField( max_length=8, default=None )
    date_joined = models.DateTimeField( 'date joined', default=timezone.now )
    is_active = models.BooleanField( 'active', default=True )
    is_admin = models.BooleanField( default=False )
    is_staff = models.BooleanField( default=False )
    receive_newsletter = models.BooleanField( 'receive newsletter', default=True )
    thumbnail = models.ImageField( upload_to=upload_thumbnail, null=True, blank=True )
    subscriptions = models.ManyToManyField( 'Subscription', through='USerSubscription', related_name='subs' )

    objects = UserManager()

    def get_full_name( self ):
        full_name = '%s %s' % ( self.first_name, self.last_name )
        return full_name.strip( )

    def get_short_name( self ):
        return self.first_name

    def __unicode__( self ):
        return self.email



class USerSubscription( models.Model ):

    class Meta:
        db_table = 'USerSubscription'

    creation_date = models.DateTimeField( 'creation_date', default=timezone.now )
    begin_date = models.DateTimeField( 'begin_date', default=timezone.now )
    end_date = models.DateTimeField( default=None, blank=True, null=True )
    price = models.DecimalField( max_digits=6, decimal_places=2 )
    subscription = models.ForeignKey( Subscription, related_name='USerSubscription' )
    user = models.ForeignKey( User, related_name='USerSubscription' )
    type = models.CharField(max_length=100)

    def __unicode__(self):
        return "{} subscribes {} (price {})" % ( self.user, self.subscription, self.price )



class Document( models.Model ):
    class Meta:
        db_table = 'Document'

    slug = models.SlugField( max_length=50 )
    user = models.ForeignKey( User )
    document_type = "Generic"
    level = models.ForeignKey( ClassLevel, null=False, default=1 )
    school = models.ForeignKey( School, null=False, default=1 )
    nb_views = models.IntegerField( default=0 )
    name = models.CharField( max_length=100 )
    matter = models.ForeignKey( ClassTopic, null=False, default=1 )
    status = models.IntegerField( choices=DOCUMENT_STATUS, default=1 )
    creation_date = models.DateTimeField( auto_now_add=True )
    deletion_date = models.DateTimeField( null=True, default=None )
    document_thumbnail = models.ImageField( upload_to=upload_document_thumbnail, default=None )

    def __unicode__( self ):
        return self.name + " (" + str( self.status ) + ") " + self.school.name



class DocumentFile( models.Model ):
    class Meta:
        db_table = 'DocumentFile'

    description = models.CharField( max_length=50, null=True )
    image = models.ImageField( upload_to=upload_function, verbose_name='image', )
    document = models.ForeignKey( Document, default=None )

    def __unicode__( self ):
        return self.description



class Exam( Document ):

    EXAM_TYPE_REAL = 'R'
    EXAM_TYPE_MOCK = 'M'
    EXAM_TYPE_COMMON = 'C'
    EXAM_TYPES = ( ( EXAM_TYPE_REAL, _( 'real' ) ),
                   ( EXAM_TYPE_MOCK, _( 'mock' ) ),
                   ( EXAM_TYPE_COMMON, _( 'common' ) ), )

    def create_exam( self, user_id, level_id, school_id, matter_id, year_exam, exam_type, **kwargs ):

        exam = self.model( user_id=user_id, level_id=level_id, school_id=school_id, matter_id=matter_id,
                           year_exam=year_exam, exam_type=exam_type )
        return exam

    class Meta:
        db_table = 'Exam'

    year_exam = models.IntegerField( choices=EXAM_YEAR_CHOICES, default='2016' )
    exam_type = models.CharField( _('exam_type'), choices=EXAM_TYPES, max_length=1, default=EXAM_TYPE_REAL )
    document_type = "Exam"

    def __unicode__( self ):
        return self.name + " " + self.matter.name

    def save( self, *args, **kwargs ):
        if not self.id:
            # Newly created object, so set slug
            slug_text = "{} {} {} {} {}".format( self.school.name, self.level.name,
                                                 self.level.sub_category, self.year_exam, self.exam_type )
            self.slug = self.name = slugify( slug_text )

        super( Exam, self ).save( *args, **kwargs )



class Correction( Document ):
    class Meta:
        db_table = 'Correction'

    #exam = models.ForeignKey( Exam )
    text = models.TextField( max_length=1024 )
    document_type = "Correction"

    def __unicode__( self ):
        return _( u"{} correction du sujet {}".format( self.id, Exam.id ) )



class Read( models.Model ):
    class Meta:
        db_table = 'Read'

    read_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( Document, related_name='read_document' )
    user = models.ForeignKey( User, related_name='read_user' )

    def __unicode__( self ):
        return self.user.email + " - " + self.document.name + " (" + str( self.read_date ) + ")"



class Submit( models.Model ):
    class Meta:
        db_table = 'Submit'

    submit_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( Document, related_name='submit_document' )
    user = models.ForeignKey( User, related_name='submit_user' )

    def __unicode__( self ):
        return "{} {} {}".format( self.user.email, self.document.name, self.submit_date )



class Comment( models.Model ):
    class Meta:
        db_table = 'Comment'

    comment_date = models.DateTimeField( auto_now_add=True )
    comment = models.TextField( max_length=512 )
    document = models.ForeignKey( Document, related_name='comment_document' )
    user = models.ForeignKey( User, related_name='comment_user' )

    def __unicode__( self ):
        return "{} {} {} {}".format( self.user.email, self.document.name, self.comment, self.comment_date )

