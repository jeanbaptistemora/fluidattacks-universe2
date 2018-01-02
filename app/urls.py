"""
    Archivo para relacion de rutas entre consultas http y vistas de django
"""

# pylint: disable=E0402
from . import views
from . import services
from django.conf.urls import url, include, handler400, handler403, handler404, handler500

# pylint: disable=W0104
handler400, handler403, handler404, handler500;

handler400 = 'app.views.error500'
handler401 = 'app.views.error401'
handler403 = 'app.views.error401'
handler404 = 'app.views.error500'
handler500 = 'app.views.error500'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Procesamiento principal
    url(r'^index/?$', views.index, name='index'),
    url(r'^error500/?$', views.error500, name='error500'),
    url(r'^error401/?$', views.error401, name='error401'),
    url(r'^login/?$', services.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^registration/?$', views.registration, name='registration'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # Presentacion Dashboard
    url(r'^get_myprojects/?\.*$', views.get_myprojects, name='get_myprojects'),
    url(r'^get_myevents/?\.*$', views.get_myevents, name='get_myevents'),
    # Consumo de servicios de formstack
    url(r'^get_finding/?\.*$', views.get_finding, name='get_finding'),
    url(r'^get_findings/?\.*$', views.get_findings, name='get_findings'),
    url(r'^get_eventualities/?\.*$',
        views.get_eventualities, name='get_eventualities'),
    url(r'^project/([A-Za-z0-9]+)/([0-9]+)/([A-Za-z.=]+)/(?P<fileid>[A-Za-z0-9._-]{20,})?$', views.get_evidences),
    url(r'^get_exploit/?\.*$', views.get_exploit, name='get_exploit'),
    url(r'^update_eventuality/?\.*$',
        views.update_eventuality, name='update_eventuality'),
    url(r'^delete_finding/?\.*$', views.delete_finding, name='delete_finding'),
    url(r'^finding_solved/?\.*$', views.finding_solved, name='finding_solved'),
    url(r'^update_cssv2/?$', views.update_cssv2, name='update_cssv2'),
    url(r'^update_description/?$', views.update_description, name='update_description'),
    url(r'^update_treatment/?$', views.update_treatment, name='update_treatment'),
    # Documentacion automatica
    url(r'^pdf/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/(?P<doctype>[a-z]+)/?$', views.project_to_pdf),
    url(r'^generate_autodoc/?$',
        views.generate_autodoc, name='generate_autodoc'),
    url(r'^export_autodoc/?$', views.export_autodoc, name='export_autodoc')
]
