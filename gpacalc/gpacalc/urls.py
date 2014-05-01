from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.views import create_semester, update_semester, SemestersIndex


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', SemestersIndex.as_view()),
    url(r'^new/semester/$', create_semester),
    url(r'^update/semester/(?P<pk>\w+)/$', update_semester),
    url(r'^admin/', include(admin.site.urls)),
)
