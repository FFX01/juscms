from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<path>[a-zA-Z0-9\-\/]+)$',
        views.BaseView.as_view(),
        name='base_view',
    ),
]
