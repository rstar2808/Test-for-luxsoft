# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings


def menu(request):

    def filter_acl(items, user):
        return [item for item in items if not 'acl' in item or item['acl'](user)]

    menu = [
        {
            'title': u'Goods',
            'url': "#",
            'submenu': [
                {
                    'title': u'Goods list',
                    'url': reverse("goods_list"),
                },
                {
                    'title': u'Product add',
                    'url': reverse("product_edit"),
                },
            ],
        },
        {
            'title': u'Taxes',
            'url': "#",
            'submenu': [
                {
                    'title': u'Taxes list',
                    'url': reverse("taxes_list"),
                },
                {
                    'title': u'Taxes add',
                    'url': reverse("tax_edit"),
                },
            ],
        },
    ]

    for item in menu:
        if 'submenu' in item:
            item['submenu'] = filter_acl(item['submenu'], request.user)

    menu = filter_acl([item for item in menu if not 'submenu' in item or item['submenu']], request.user)  # purge items with empty submenu

    return {
        'menu': menu,
    }
