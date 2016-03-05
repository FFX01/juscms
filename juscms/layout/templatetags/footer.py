from django import template

from layout.models import Footer


register = template.Library()


@register.inclusion_tag('footer.html')
def render_footer():
    footer = Footer.objects.all()[:1]
    return {
        'footer': footer,
    }
