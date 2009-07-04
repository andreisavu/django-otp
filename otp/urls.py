from django.conf.urls.defaults import *

from otp.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', home),
    (r'^secret-page$', secret_page),
    (r'^login$', login),
    (r'^logout$', logout),
    (r'^register$', register),
    # Example:
    # (r'^otp/', include('otp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
