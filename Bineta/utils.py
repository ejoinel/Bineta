# -*- coding: utf-8 -*-

import random
import string
from shutil import copyfile

import os
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import loader

import settings



def remove_accents_spaces( ligne ):
    """ supprime les accents du texte source """
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                'e': ['é', 'è', 'ê', 'ë'],
                'i': ['î', 'ï'],
                'u': ['ù', 'ü', 'û'],
                'o': ['ô', 'ö'],
                ' ': ['_']}
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            ligne.replace(accented_char, char)
    return ligne



def send_email(to_email, from_email, context, subject,
               plain_body_template_name=None, html_body_template_name=None):
    assert plain_body_template_name or html_body_template_name

    if plain_body_template_name:
        plain_body = loader.render_to_string(plain_body_template_name, context)
        email_message = EmailMultiAlternatives(subject, plain_body, from_email, [to_email])
        if html_body_template_name:
            html_body = loader.render_to_string(html_body_template_name, context)
            email_message.attach_alternative(html_body, 'text/html')
    else:
        html_body = loader.render_to_string(html_body_template_name, context)
        email_message = EmailMessage(subject, html_body, from_email, [to_email])
        email_message.content_subtype = 'html'

    email_message.send()



def generate_code( pass_length=settings.PASSWORD_MIN_LENGTH ):

    chars = string.ascii_uppercase + string.digits
    return ''.join( random.choice(chars) for _ in range( pass_length ) )



def get_random_image( icons_dir=settings.MEDIA_IMAGE_PROFILE_MEN ):

    """returns the filename of a randomly chosen image in dir"""
    images = [ f for f in os.listdir( icons_dir ) if f.endswith( ".jpg" ) or f.endswith( ".png" ) ]
    return os.path.join( icons_dir, random.choice( images ) )



def copy_file_in_media(src_file):
    dest_file = os.path.join( settings.MEDIA_IMAGES_PROFILE, os.path.basename( src_file ) )
    copyfile(src_file, dest_file)
    return dest_file
