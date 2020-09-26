from django import template
from django.conf import settings

register = template.Library()

# https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/

# settings value
@register.simple_tag(name="get_settings")
def get_settings(var_name):
    return getattr(settings, var_name, "")

# Usage:
# {% settings_value "LANGUAGE_CODE" %}


@register.simple_tag(name="quotation_liked_by")
def quotation_liked_by(quotation, user):
    return quotation.is_liked_by(user)

@register.simple_tag(name="quotation_favorited_by")
def quotation_favorited_by(quotation, user):
    return quotation.is_favorited_by(user)
