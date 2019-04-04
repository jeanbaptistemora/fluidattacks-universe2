""" File for linking routes between http queries and django views. """

# pylint: disable=E0402
from __future__ import absolute_import

from django.conf.urls import url, include, handler400, handler403, handler404, handler500
from django.conf import settings
from graphene_django.views import GraphQLView
from .entity import schema
from . import views
from . import services

# pylint: disable=W0104
handler400, handler403, handler404, handler500

# pylint: disable=invalid-name
handler400 = 'app.views.error500'
handler401 = 'app.views.error401'
handler403 = 'app.views.error401'
handler404 = 'app.views.error500'
handler500 = 'app.views.error500'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Principal process.
    url(r'^index/?$', views.index, name='index'),
    url(r'^error500/?$', views.error500, name='error500'),
    url(r'^error401/?$', views.error401, name='error401'),
    url(r'^login/?$', services.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^registration/?$', views.registration, name='registration'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^forms/?\.*$', views.forms),
    url(r'^api/?\.*$',
        GraphQLView.as_view(graphiql=True if settings.DEBUG else False, schema=schema.SCHEMA)),
    # Project view.
    url(r'^project_findings/?\.*$', views.project_findings),
    url(r'^project_drafts/?\.*$', views.project_drafts),
    url(r'^project_events/?\.*$', views.project_events),
    # Dashboard view.
    url(r'^get_myprojects/?\.*$', views.get_myprojects, name='get_myprojects'),
    url(r'^get_drafts/?\.*$', views.get_drafts, name='get_drafts'),
    # Use of Formstack services.
    url(r'^get_findings/?\.*$', views.get_findings, name='get_findings'),
    url(r'^access_to_project/?\.*$', views.access_to_project, name='access_to_project'),
    url(r'^project/(?P<project>[A-Za-z0-9]+)/(?P<findingid>[0-9]+)/([A-Za-z.=]+)/(?P<fileid>[A-Za-z0-9._-]+)?$',  # noqa
        views.get_evidence),
    url(r'^(?P<findingid>[0-9]+)/download_vulnerabilities?$', views.download_vulnerabilities),
    url(r'^is_customer_admin/?\.*$', views.is_customer_admin, name='is_customer_admin'),
    # Documentation.
    url(r'^pdf/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/(?P<doctype>[a-z]+)/?$',
        views.project_to_pdf),
    url(r'^xls/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/?$',
        views.project_to_xls),
    url(r'^check_pdf/project/(?P<project>[A-Za-z0-9]+)/?$', views.check_pdf),
]
