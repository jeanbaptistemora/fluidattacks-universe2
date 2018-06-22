""" File for linking routes between http queries and django views. """

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
    # Principal process.
    url(r'^index/?$', views.index, name='index'),
    url(r'^error500/?$', views.error500, name='error500'),
    url(r'^error401/?$', views.error401, name='error401'),
    url(r'^login/?$', services.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^registration/?$', views.registration, name='registration'),
    url(r'^is_registered/?$', views.is_registered, name='is_registered'),
    url(r'^legal_status/?$', views.legal_status, name='legal_status'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^forms/?\.*$', views.forms),
    url(r'^api/?\.*$', views.graphql_api, name='graphql_api'),
    # Project view.
    url(r'^project_indicators/?\.*$', views.project_indicators),
    url(r'^project_findings/?\.*$', views.project_findings),
    url(r'^project_releases/?\.*$', views.project_releases),
    url(r'^project_events/?\.*$', views.project_events),
    url(r'^project_users/?\.*$', views.project_users),
    # Comments tab.
    url(r'^get_comments/?\.*$', views.get_comments, name='get_comments'),
    url(r'^add_comment/?\.*$', views.add_comment, name='add_comment'),
    url(r'^delete_comment/?\.*$', views.delete_comment, name='delete_comment'),
    # Dashboard view.
    url(r'^get_myprojects/?\.*$', views.get_myprojects, name='get_myprojects'),
    url(r'^get_myevents/?\.*$', views.get_myevents, name='get_myevents'),
    url(r'^get_releases/?\.*$', views.get_releases, name='get_releases'),
    # Use of Formstack services.
    url(r'^get_finding/?\.*$', views.get_finding, name='get_finding'),
    url(r'^get_findings/?\.*$', views.get_findings, name='get_findings'),
    url(r'^total_severity/?\.*$', views.total_severity, name='total_severity'),
    url(r'^get_eventualities/?\.*$',
        views.get_eventualities, name='get_eventualities'),
    url(r'^get_evidences/?\.*$', views.get_evidences, name='get_evidences'),
    url(r'^get_users_login/?\.*$', views.get_users_login, name='get_users_login'),
    url(r'^add_access_integrates/?\.*$', views.add_access_integrates, name='add_access_integrates'),
    url(r'^remove_access_integrates/?\.*$', views.remove_access_integrates, name='remove_access_integrates'),
    url(r'^change_user_role/?\.*$', views.change_user_role, name='change_user_role'),
    url(r'^get_alerts/?\.*$', views.get_alerts, name='get_alerts'),
    url(r'^project/([A-Za-z0-9]+)/(?P<findingid>[0-9]+)/([A-Za-z.=]+)/(?P<fileid>[A-Za-z0-9._-]+)?$', views.get_evidence),
    url(r'^get_exploit/?\.*$', views.get_exploit, name='get_exploit'),
    url(r'^get_records/?\.*$', views.get_records, name='get_records'),
    url(r'^update_eventuality/?\.*$',
        views.update_eventuality, name='update_eventuality'),
    url(r'^delete_finding/?\.*$', views.delete_finding, name='delete_finding'),
    url(r'^accept_release/?\.*$', views.accept_release, name='accept_release'),
    url(r'^reject_release/?\.*$', views.reject_release, name='reject_release'),
    url(r'^finding_solved/?\.*$', views.finding_solved, name='finding_solved'),
    url(r'^update_cssv2/?$', views.update_cssv2, name='update_cssv2'),
    url(r'^update_description/?$', views.update_description, name='update_description'),
    url(r'^update_evidence_text/?$', views.update_evidence_text, name='update_evidence_text'),
    url(r'^update_treatment/?$', views.update_treatment, name='update_treatment'),
    url(r'^get_remediated/?$', views.get_remediated, name='get_remediated'),
    url(r'^finding_verified/?\.*$', views.finding_verified, name='finding_verified'),
    url(r'^update_evidences_files/?\.*$', views.update_evidences_files, name='update_evidences_files'),
    # Documentation.
    url(r'^pdf/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/(?P<doctype>[a-z]+)/?$', views.project_to_pdf),
    url(r'^xls/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/?$', views.project_to_xls),
    url(r'^check_pdf/project/(?P<project>[A-Za-z0-9]+)/?$', views.check_pdf)
]
