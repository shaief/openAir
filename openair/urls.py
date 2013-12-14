from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()   

urlpatterns = patterns('',
    url(r'^', TemplateView.as_view(template_name="records/index.html"), name='home'),
    # Examples:
    # url(r'^$', 'openair.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
