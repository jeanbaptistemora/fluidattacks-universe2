"""File for linking routes between http queries and django views."""

from django.conf.urls import (
    url,
    include,
    handler400,
    handler403,
    handler404,
    handler500
)
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from backend.api.schema import SCHEMA
from backend.api.view import APIView
from backend.decorators import verify_csrf

from app import views

# pylint: disable=pointless-statement
handler400, handler403, handler404, handler500

# pylint: disable=invalid-name
handler400 = 'app.views.error401'
handler401 = 'app.views.error401'
handler403 = 'app.views.error401'
handler404 = 'app.views.error401'
handler500 = 'app.views.error500'


@csrf_exempt  # type: ignore
def api_dispatcher(request: HttpRequest) -> HttpResponse:
    # Answer preflight requests properly
    #   see: https://gitlab.com/fluidattacks/integrates/-/issues/1958
    if request.method == 'OPTIONS':
        response = HttpResponse()
    else:
        response = verify_csrf(APIView.as_view(schema=SCHEMA))(request)
        response['Content-Type'] += '; charset=utf-8'

    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = '*'
    return response


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/?$', views.index, name='index'),
    # Principal process.
    url(r'^graphic/?$', views.graphic, name='graphic'),
    url(
        r'^graphics-for-group/?$',
        views.graphics_for_group,
        name='graphics_for_group'
    ),
    url(
        r'^graphics-for-organization/?$',
        views.graphics_for_organization,
        name='graphics_for_organization'
    ),
    url(
        r'^graphics-for-portfolio/?$',
        views.graphics_for_portfolio,
        name='graphics_for_portfolio'
    ),
    url(r'^graphics-report/?$', views.graphics_report, name='graphics_report'),
    url(r'^error500/?$', views.error500, name='error500'),
    url(r'^error401/?$', views.error401, name='error401'),
    url(r'^mobile/?$', views.mobile, name='mobile'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^api/?\.*$', api_dispatcher),
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
    ),
    # Confirm access to group
    url(
        r'^confirm_access/(?P<urltoken>[A-Za-z0-9\._-]+)?$',
        views.confirm_access
    ),
    # Let the front router handle them
    url(r'', views.app),
]
