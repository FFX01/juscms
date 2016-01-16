from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Page


class BaseView(View):
    def get(self, request, path):
        instance = get_object_or_404(Page, path=path)
        context = {
            'instance': instance,
        }
        return render(
            request,
            instance.template,
            context,
        )



