import calendar
import datetime

from django import template

register = template.Library()


@register.filter
def add_css_classes_if_invalid(field, css_classes):
    if field.errors:
        css_classes += ' is-invalid'
    return field.as_widget(attrs={'class': css_classes})


@register.filter
def format_value(val):
    formatted_value = 'R$ {:,.2f}'.format(val).replace(',', ' ').replace('.', ',').replace(' ', '.').replace(
        'R$.', 'R$ ')
    return formatted_value


@register.filter(name='add_months')
def add_months(value, months):
    """
    Adds the specified number of months to a date.

    Usage:
    {{ some_date_variable|add_months:number_of_months }}
    """
    if value and isinstance(value, (datetime.date, datetime.datetime)):
        year = value.year + (value.month + months - 1) // 12
        month = (value.month + months - 1) % 12 + 1
        day = min(value.day, calendar.monthrange(year, month)[1])
        return value.replace(year=year, month=month, day=day)
    return value


@register.filter(name='custom_range')
def custom_range(value):
    return range(value)
