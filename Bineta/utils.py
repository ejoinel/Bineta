# -*- coding: utf-8 -*-

import os
import settings
import binascii
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import loader


def remove_accents_spaces(self, ligne):
    """ supprime les accents du texte source """
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                'e': ['é', 'è', 'ê', 'ë'],
                'i': ['î', 'ï'],
                'u': ['ù', 'ü', 'û'],
                'o': ['ô', 'ö'],
                ' ': ['_']}
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            ligne = ligne.replace(accented_char, char)
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
    return binascii.hexlify( os.urandom( pass_length ) )
