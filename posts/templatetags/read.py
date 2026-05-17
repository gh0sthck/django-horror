from django import template

register = template.Library()


@register.filter
def get_readable_comments(value_s: str):
    value_i = int(value_s)
    if value_i != 11 and value_i % 10 == 1:
        return "комментарий"
    if value_i >= 11 and value_i <= 20:
        return "комментариев"
    if value_i % 10 >= 2 and value_i % 10 < 5:
        return "комментария"
    else:
        return "комментариев"


@register.filter
def get_readable_views(value_s: str):
    value_i = int(value_s)
    if value_i != 11 and value_i % 10 == 1:
        return "просмотр"
    if value_i >= 11 and value_i <= 20:
        return "просмотров"
    if value_i % 10 >= 2 and value_i % 10 < 5:
        return "просмотра"
    else:
        return "просмотров"
