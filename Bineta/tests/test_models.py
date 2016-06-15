# -*- coding: utf-8 -*-

import nose.tools as nt

import factory
from django.test import TestCase

from Bineta.models import User, Exam, School, Subscription
from Bineta.bineta_api import UserViewSet, PasswordReset, CreateUser, ExamViewSet, CreateExam, Exam_list, exam_add_photo

from django.test import Client

class TestModels( object ):

    def setup( self ):

        print 'setUp()'

        self.client = Client()

        self.simple_user = User.objects.create_simple_user( email="simple_user@bineta.com",
                                                            password="password_simple_user",
                                                            last_name="simple_last_name",
                                                            first_name="simple_first_name", gender="M",
                                                            birth_date="2014-01-01", school_id=1)

        nt.assert_is_not_none( self.simple_user, "Error creating simple user")

        print "Simple_User : {}".format( self.simple_user)

        self.super_user = User.objects.create_simple_user( email="simple_user@bineta.com",
                                                           password="password_simple_user",
                                                           last_name="simple_last_name", first_name="simple_first_name",
                                                           gender="M", birth_date="2014-01-01", school_id=1)

        nt.assert_is_not_none( self.simple_user, "Error creating super user")

        self.super_user.is_admin = True
        self.super_user.is_staff = True
        self.super_user.save()

        print "Super_User : {}".format( self.super_user)
