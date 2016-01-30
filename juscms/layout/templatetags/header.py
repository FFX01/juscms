from django import template

from layout.models import Header


register = template.Library()


@register.inclusion_tag('header.html')
def render_header():
    header = Header.objects.all()[:1]
    return {
        'header': header,
    }