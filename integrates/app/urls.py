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
    url(r'^new/?$', views.index, name='new')
]
