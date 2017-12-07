'''
Store all utility functions!
'''

from django.shortcuts import _get_queryset
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from html2text import html2text
from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings

def send_email(kwargs):
    '''
        Send emauls!
    '''
    send_mail(kwargs['subject'],
              kwargs['message'],
              kwargs['from_mail'],
              kwargs['to_mails'],
              fail_silently=False)


def send_mail_html(subject, to_address, html_name, text_name, context_dict=dict(), bcc=[]):
    '''
    Send mail in html format by passing html and test file names with context dict.
    '''

    print(context_dict, "context_dict")
    body_template = get_template(html_name)
    body_html = body_template.render(context_dict)
    body_text = html2text(get_template(text_name) \
                          .render(context_dict))
    email = EmailMultiAlternatives(
        subject=subject,
        body=body_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_address,
        bcc=bcc)

    email.attach_alternative(body_html, "text/html")
    email.mixed_subtype = 'related'
    email.send()

def get_object_or_None(klass, *ar, **kw):
    '''
    Returns object if it exists or None.

    kclass may be Model, Manager, Object.
    '''
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*ar, **kw)
    except queryset.model.DoesNotExist:
        return None

def get_base_url(request):
    transfer_protocol = 'http' if settings.DEBUG else 'https'
    return '%s://%s' % (transfer_protocol, get_current_site(request).domain)