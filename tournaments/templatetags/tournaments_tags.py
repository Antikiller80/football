from django import template
from tournaments.models import position_choices


def get_position_display(value):
    for choice in position_choices:
        if choice[0] == value:
            return choice[1]
    else:
        return 'Нет такой позиции'

register = template.Library()

register.filter("get_position_display", get_position_display)
