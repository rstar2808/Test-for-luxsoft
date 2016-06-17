from django.conf.urls import patterns, include, url
from shop_taxes.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('shop_taxes.views',
                       url(r'^$', 'home', name="home"),
                       url(r'^register/$', register, name='register'),
                       url(r'^goods_list/$', goods_list, name='goods_list'),
                       url(r'^logout/$', logout_view, name='logout'),
                       url(r'^login/$', login_view, name='login'),

                      )
    # Examples:
    # url(r'^$', 'shop_taxes.views.home', name='home'),
    # url(r'^shop_taxes/', include('shop_taxes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
