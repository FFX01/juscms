from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import Page


class PageTest(TestCase):

    def test_page_can_be_retrieved(self):

        client = Client()

        page = Page(
            title='Test Page',
            is_home=False
        )

        page.save()

        page = Page.objects.get(id=1)

        url = reverse(
            'pages:base_view',
            kwargs={'path': page.path}
        )

        response = client.get(path=url)

        self.assertEqual(
            response.status_code,
            200
        )
