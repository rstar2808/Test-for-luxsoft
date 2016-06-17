# -*- coding: utf-8 -*-

from annoying.decorators import render_to
from django.contrib.auth import login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json
import django_couch
from shop_taxes.forms import *
from shop_taxes.models import *


@render_to('shop_taxes/home.html')
def home(request):
    if request.is_ajax():
        if 'product_id' in request.GET and request.GET['product_id']:
            product, category = None, None

            try:
                product = request.db[request.GET['product_id']]
                category = request.db[product['category']]
                status = 'OK'
            except:
                status = 'ERROR'

            return HttpResponse(
                json.dumps({'status': status, 'cost': product['cost'], 'tax': category['procent'], 'name': product['name']}),
                content_type='application/json'
            )
    category = []
    goods = [row.doc for row in request.db.view('goods/list', include_docs=True).rows]
    for product in goods:
        if product['category'] not in category:
            category.append(product['category'])
    category = {row.id: row.doc.name for row in request.db.view('_all_docs', keys=category, include_docs=True).rows}
    return {
        'goods': goods,
        'category': category,
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
    print 1
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
    category = []
    goods = [row.doc for row in request.db.view('goods/list', include_docs=True).rows]
    for product in goods:
        if product['category'] not in category:
            category.append(product['category'])
    category = {row.id: row.doc.name for row in request.db.view('_all_docs', keys=category, include_docs=True).rows}
    return {
        'goods': goods,
        'category': category,
    }


@login_required()
@render_to('shop_taxes/taxes_list.html')
def taxes_list(request):

    taxes = [row.doc for row in request.db.view('taxes/list', include_docs=True).rows]

    return {
        'taxes': taxes,
    }



@login_required()
@render_to('shop_taxes/tax_edit.html')
def tax_edit(request, tax_id=None):
    if tax_id:
        tax = Tax.load(tax_id)

    else:
        tax = Tax(_db=request.db)
    form = TaxEditForm(request.POST or None, initial=tax)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            tax.update(data)
            if tax_id:
                tax.save()
            else:
                tax.create("t_%s" % django_couch.slugify(data['name']))
            return redirect('taxes_list')
    return {
        'form': form,
        'tax': tax
    }

@login_required()
@render_to('shop_taxes/product_edit.html')
def product_edit(request, product_id=None):
    if product_id:
        product = Product.load(product_id)
    else:
        product = Product(_db=request.db)

    taxes = [(row.id, row.key) for row in request.db.view('taxes/list').rows]

    form = ProductEditForm(request.POST or None, initial=product, category=taxes)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            product.update(data)
            if product_id:
                product.save()
            else:
                product.create("p_%s" % django_couch.slugify(data['name']))
            return redirect('goods_list')
    return {
        'form': form,
        'product': product
    }
# Создание и редактирование товаров

# Список товаров и добавление в корзину

