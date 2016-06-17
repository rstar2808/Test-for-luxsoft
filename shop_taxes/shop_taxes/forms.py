# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django import forms
import django_couch


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not (username and password):
            return

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                return user
            else:
                raise forms.ValidationError(u"Your account is not active, please contact the site admin.")
        else:
            raise forms.ValidationError(u"Your username and/or password were incorrect.")


class AddUserForm(forms.Form):

    username = forms.EmailField(label='E-mail', widget=forms.TextInput(), required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), required=True)

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(), required=True)

    # email should be unique.
    def clean_username(self):
        db = django_couch.db()
        username = self.cleaned_data['username']
        rows = db.view('auth/all', key=username).rows
        if rows:
            raise forms.ValidationError(_('This username is already used'))
        else:
            return username.lower()

    # passwords must be same
    def clean_password2(self):
        if self.cleaned_data.get('password1', '') != self.cleaned_data.get('password2', ''):
            raise forms.ValidationError(_("Passwords don't match"))
        return self.cleaned_data['password2']


class TaxEditForm(forms.Form):
    is_active = forms.BooleanField(label=u'Active', required=False)
    name = forms.CharField(label='Name', widget=forms.TextInput(), required=True)
    procent = forms.IntegerField(label='Procent', required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=True)


class ProductEditForm(forms.Form):
    is_active = forms.BooleanField(label=u'Active', required=False)
    name = forms.CharField(label='Name', widget=forms.TextInput(), required=True)
    cost = forms.FloatField(label='Cost', required=True)
    category = forms.ChoiceField(label='Category', choices=[], required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=True)

    def __init__(self, *args, **kwargs):
        category = []
        if 'category' in kwargs:
            category = kwargs['category']
            del kwargs['category']
        super(ProductEditForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = category