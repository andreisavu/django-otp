from django.conf.urls.defaults import *

from otp.views import *

import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', home),
    (r'^secret-page$', secret_page),
    (r'^login$', login),
    (r'^logout$', logout),
    (r'^register$', register),
    (r'^onetime$', onetime),
    (r'^onetime_login$', onetime_login),
    (r'^modify_account$', modify_account),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/'.join([os.path.dirname(__file__), 'static'])}),

    url(r'^captcha/', include('captcha.urls')),

    # Example:
    # (r'^otp/', include('otp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
