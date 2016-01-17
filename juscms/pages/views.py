from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Page


class BaseView(View):
    def get(self, request, path):
        """
        This method is called when a client machine requests a url
        that fits the url pattern to call basic content pages.

        Parameters:
            self(class): The class that calls this method. In this case it is
                the baseview class.
            request(object): The http request object as received by the server
                the client.
            path(string): The path captured in the request url as defined in
                pages/urls.py. This parameter is used to retrieve a page
                instance to render.

        Returns(function): The render function used to pass variables to the
            HTML template which is generated and sent to the client machine.
        """
        instance = get_object_or_404(Page, path=path)
        context = {
            'instance': instance,
        }
        return render(
            request,
            instance.template,
            context,
        )



