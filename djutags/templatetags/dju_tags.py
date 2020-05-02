# -*- coding: utf-8 -*-

from __future__ import with_statement
from classytags.arguments import IntegerArgument, Argument, StringArgument
from classytags.core import Options
from classytags.helpers import InclusionTag
from datetime import datetime
#from cms.utils.i18n import force_language, get_language_objects
from django import template
from django.contrib.sites.models import Site
from django.urls import reverse, NoReverseMatch
from django.utils.encoding import force_text
from django.utils.six.moves.urllib.parse import unquote
from django.utils.translation import get_language, ugettext

#from menus.menu_pool import menu_pool
#from menus.utils import DefaultLanguageChanger
from django.utils.translation import get_language

from django.conf import settings


register = template.Library()

@register.filter
def SetBodyClass(path):
    """
    defines a body class according to path
    """

    bodyclass = "campl-theme-3"

    if "departement-1" in path or "department-1" in path:
        bodyclass = "campl-theme-2"

    elif "departement-2" in path or "department-2" in path:
        bodyclass = "campl-theme-5"

    elif "departement-3" in path or "department-3" in path:
        bodyclass = "campl-theme-6"

    elif "departement-4" in path or "department-4" in path:
        bodyclass = "campl-theme-1"

    
    return bodyclass


def dju_env(name):
    ret = getattr(settings, name, "")
    return ret

register.simple_tag(dju_env)


def dju_env_short(name):
    return getattr(settings, name, "")[0:8]

register.simple_tag(dju_env_short)


#######################
# Tests dans snippets #
#######################

import datetime

# Version simple 

@register.simple_tag
def dju_current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


# Version avancée https://docs.djangoproject.com/fr/1.10/howto/custom-template-tags/#advanced-custom-template-tags

class CurrentTimeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string
    def render(self, context):
        return datetime.datetime.now().strftime(self.format_string)


def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return CurrentTimeNode(format_string[1:-1])


register.tag('dju_advanced_current_time', do_current_time)



class DjuEnvNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        print("name = " + str(self.varname))
        ret = getattr(settings, self.varname, "")
        print("ret = " + str(ret))
        return ret

@register.tag(name='dju_env_v2')
def do_dju_env_v2(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, varname_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )
    if not (varname_string[0] == varname_string[-1] and
            varname_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return DjuEnvNode(varname_string[1:-1])


from classytags.core import Tag
class HelloWorld(Tag):
    name = 'classy_hello_world'
    def render_tag(self, context):
        return 'hello classy world'
register.tag(HelloWorld)


def simple_hello_world():
    return 'hello simple world'
register.simple_tag(simple_hello_world)


#####################
# Classy Tags tests #
#####################

#from classytags.core import Tag
#from django import template

#class HelloWorld(Tag):
#    name = 'hello_classy_world'

#    def render_tag(self, context):
#        return 'hello world'

#register.tag(HelloWorld)
