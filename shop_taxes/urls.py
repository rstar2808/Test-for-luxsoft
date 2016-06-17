from django.conf import settings
from django.views import static
from django.conf.urls import *


urlpatterns = patterns('',
                       (r'^', include('shop_taxes.urls')),
                       (r"^media/(.+)", static.serve, {"document_root": settings.MEDIA_ROOT}),
                      )