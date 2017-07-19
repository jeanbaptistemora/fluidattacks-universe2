"""
    Archivo para relacion de rutas entre consultas http y vistas de django
"""

# pylint: disable=E0402
from . import views
from . import services
from django.conf.urls import url, include, handler400, handler403, handler404, handler500

# pylint: disable=W0104
handler400, handler403, handler404, handler500;

handler400 = 'app.views.error'
handler403 = 'app.views.error'
handler404 = 'app.views.error'
handler500 = 'app.views.error'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Procesamiento principal
    url(r'^index/?$', views.index, name='index'),
    url(r'^error/?$', views.error, name='error'),
    url(r'^login/?$', services.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^registration/?$', views.registration, name='registration'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # Consumo de servicios de formstack
    url(r'^get_finding/?\.*$', views.get_finding, name='get_finding'),
    url(r'^get_findings/?\.*$', views.get_findings, name='get_findings'),
    url(r'^get_eventualities/?\.*$',
        views.get_eventualities, name='get_eventualities'),
    url(r'^update_finding/?\.*$', views.update_finding, name='update_finding'),
    url(r'^update_eventuality/?\.*$',
        views.update_eventuality, name='update_eventuality'),
    url(r'^delete_finding/?\.*$', views.delete_finding, name='delete_finding'),
    url(r'^get_order/?\.*$', views.get_order, name='get_order'),
    url(r'^update_order/?\.*$', views.update_order, name='update_order'),
    # Documentacion automatica
    url(r'^generate_autodoc/?$',
        views.generate_autodoc, name='generate_autodoc'),
    url(r'^export_autodoc/?$', views.export_autodoc, name='export_autodoc')
]
