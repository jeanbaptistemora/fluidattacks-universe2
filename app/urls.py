from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/?$', views.index, name='index'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^get_vuln_by_name/?\.*$', views.get_vuln_by_name, name='get_vuln_by_name'),
    url(r'^get_vuln_by_date/?\.*$', views.get_vuln_by_date, name='get_vuln_by_date'),
    url(r'^get_evnt_by_name/?\.*$', views.get_evnt_by_name, name='get_evnt_by_name'),
] 