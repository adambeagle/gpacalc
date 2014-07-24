from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from core.views import (create_semester, SemesterDeleteView, 
    update_semester, SemestersIndex)


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', SemestersIndex.as_view(), name='semester_index'),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^create/semester/$', create_semester, name='create_semester'),
    url(r'^edit/semester/(?P<pk>\w+)/$', update_semester, name='update_semester'),
    url(r'^delete/semester/(?P<pk>\w+)/$', SemesterDeleteView.as_view(), name='delete_semester'),
    url(r'^admin/', include(admin.site.urls)),
)
