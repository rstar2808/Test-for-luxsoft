# -*- coding: utf-8 -*-

from annoying.decorators import render_to
from django.contrib.auth import login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import django_couch
from shop_taxes.forms import *
from shop_taxes.models import *

@login_required()
@render_to('shop_taxes/home.html')
def home(request):
    return {
        'gg': 'gg'
    }


@render_to('shop_taxes/login.html')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', None) or reverse('home'))

    else:
        form = LoginForm()

    return {
        'form': form,
    }


@render_to('shop_taxes/reg.html')
def register(request):
    """
    creating new user account and send confirmation link to email
    """
    if request.method == "POST":
        form = AddUserForm(request.POST)

        if form.is_valid():
            new_user = CustomUser({
                'username': form.cleaned_data['username'],
                'fullname': '%s %s' % (form.cleaned_data['first_name'], form.cleaned_data['last_name'])
            })
            new_user.set_password(form.cleaned_data['password2'])
            new_user.create('u_%s' % django_couch.slugify(new_user.username))
            return redirect('login')
    else:
        form = AddUserForm()

    return {
        'form': form
    }


@login_required()
def logout_view(request):

    if 'user' in request and 'id' in request['user']:
        request.META['Close_Session'] = request.user.id

    return logout(request, '/')


@login_required()
@render_to('shop_taxes/goods_list.html')
def goods_list(request):

    goods = [row.doc for row in request.db.view('goods/list', include_docs=True).rows]

    return {
        'goods': goods,
    }
# Таблица налогов и ее редактирование


# Создание и редактирование товаров

# Список товаров и добавление в корзину

