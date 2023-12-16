from django import template

register = template.Library()


@register.filter
def add_css_classes_if_invalid(field, css_classes):
    if field.errors:
        css_classes += ' is-invalid'
    return field.as_widget(attrs={'class': css_classes})


@register.filter
def format_value(val):
    float_val = float(val)
    formatted_value = 'R$ {:,.2f}'.format(float_val).replace(',', ' ').replace('.', ',').replace(' ', '.').replace(
        'R$.', 'R$ ')
    return formatted_value
