"""File for linking routes between http queries and django views."""

from django.conf.urls import url
from django.views.generic import RedirectView

from app import views


# pylint: disable=invalid-name
handler400 = 'app.views.error401'
handler401 = 'app.views.error401'
handler403 = 'app.views.error401'
handler404 = 'app.views.error401'
handler500 = 'app.views.error500'


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='new')),
    url(r'^new/?$', views.index, name='new'),

    # Evidences
    url(
        (r'^project/(?P<project>[A-Za-z0-9]+)/(?P<evidence_type>[A-Za-z0-9]+)/'
         r'(?P<findingid>[0-9]+)/([A-Za-z.=]+)/(?P<fileid>[\w\.-]+)?$'),
        views.get_evidence
    ),
    # intentionally duplicate to give support to old evidence url
    url(
        (r'^groups/(?P<project>[A-Za-z0-9]+)/(?P<evidence_type>[A-Za-z0-9]+)/'
         r'(?P<findingid>[0-9]+)/([A-Za-z.=]+)/(?P<fileid>[\w\.-]+)?$'),
        views.get_evidence
    ),
    # New group URL format including organization
    url(
        r'^orgs/[a-zA-Z]+/groups/(?P<project>[A-Za-z0-9]+)/'
        r'(?P<evidence_type>[A-Za-z0-9]+)/(?P<findingid>[0-9]+)/([A-Za-z.=]+)/'
        r'(?P<fileid>[\w\.-]+)?$',
        views.get_evidence
    )
]
