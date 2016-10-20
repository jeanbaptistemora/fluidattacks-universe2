"""
    Archivo para relacion de rutas entre consultas http y vistas de django
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/?$', views.index, name='index'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^get_vuln_by_name/?\.*$', views.get_vuln_by_name, name='get_vuln_by_name'),
    url(r'^get_evnt_by_name/?\.*$', views.get_evnt_by_name, name='get_evnt_by_name'),
    url(r'^generate_auto_doc/?$', views.generate_auto_doc, name='generate_auto_doc'),
    url(r'^update_vuln/?\.*$', views.update_vuln, name='update_vuln'),
    url(r'^update_evnt/?\.*$', views.update_evnt, name='update_evnt'),
    url(r'^delete_vuln/?\.*$', views.delete_vuln, name='delete_vuln')    
] 