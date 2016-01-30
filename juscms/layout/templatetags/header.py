from django import template

from layout.models import Header


register = template.Library()


@register.inclusion_tag('footer.html')
def render_header()