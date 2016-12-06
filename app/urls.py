"""
    Archivo para relacion de rutas entre consultas http y vistas de django
"""
from django.conf.urls import url

from . import views, errors
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Procesamiento principal
    url(r'^index/?$', views.index, name='index'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^logout/?$', views.logout, name='logout'),
    # Consumo de servicios de formstack
    url(r'^get_vuln_by_name/?\.*$', views.get_vuln_by_name, name='get_vuln_by_name'),
    url(r'^get_evnt_by_name/?\.*$', views.get_evnt_by_name, name='get_evnt_by_name'),
    url(r'^update_vuln/?\.*$', views.update_vuln, name='update_vuln'),
    url(r'^update_evnt/?\.*$', views.update_evnt, name='update_evnt'),
    url(r'^delete_vuln/?\.*$', views.delete_vuln, name='delete_vuln'),
    # Documentacion automatica
    url(r'^generate_autodoc/?$', views.generate_autodoc, name='generate_autodoc'),
    url(r'^export_autodoc/?$', views.export_autodoc, name='export_autodoc')
]
