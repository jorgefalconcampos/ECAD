#Esta template tag remarca el título/subtitulo del post según la query buscada

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='highlight')
def highlight(text, search):
    highlighted = text.replace(search, '<span class="highlight">{}</span>'.format(search))
    return mark_safe(highlighted)