# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.tag
def active(parser, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])


class NavSelectedNode(template.Node):
    def __init__(self, patterns):
        self.view_args = []
        self.view_name = patterns[0]
        if len(patterns) > 1:
            self.view_args = [patterns[1]]
    def render(self, context):
        path = context['request'].path
        pValue = reverse(template.Variable(self.view_name).resolve(context), args=self.view_args)
        if path == pValue:
            return u'active'
        return ''


@register.filter
def get(dictionary, key, default=None):
    return dictionary.get(key, default)