from django import forms
from django.contrib import admin
from django.db import models as django
from django.utils.text import Truncator
from django.utils.html import mark_safe, format_html
from django.utils.translation import ugettext_lazy as _

from . import models

@admin.register(models.Tweets)
class TweetAdmin(admin.ModelAdmin):
    icon = '<i class="fa fa-tint"></i>'
    actions = None
    list_display =[field.name for field in models.Tweets._meta.fields]

    def map(self, ocean):
        if ocean.map_url:
            return format_html('<div class="col s12 center-align"><img src="{}" width="200" /></div>', ocean.map_url)
        return ""
    map.short_description = _('map')

    def short_description(self, ocean):
        return Truncator(ocean.description).words(100, truncate=' ...')
    short_description.short_description = _('short description')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False