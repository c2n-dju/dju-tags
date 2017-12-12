# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import Site


def debug(context):
    return {'DEBUG': settings.DEBUG}


def site(context):
    """
    C'est codé dur à partir de domain en attendant que l'on définisse une table des sites contenant les acronymes
    """
    domain = Site.objects.get(id=settings.SITE_ID).domain
    SITE_ACRONYME = domain.split('.')[0] 
    if SITE_ACRONYME[0:6] == 'edith-':
        SITE_ACRONYME = SITE_ACRONYME[6:]
    if SITE_ACRONYME == 'cms':
        SITE_ACRONYME = 'www'
    return {'SITE_ACRONYME': SITE_ACRONYME}
