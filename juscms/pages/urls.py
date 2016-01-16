from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<path>.*)$',
        views.BaseView.as_view(),
        name='base_view',
    ),
]
