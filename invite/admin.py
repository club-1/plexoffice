from django.contrib import admin
from django.utils.html import format_html
from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('string', 'date_creation',
                    'date_usage', 'used_by', 'share_url')
    list_filter = ('date_usage',)
    date_hierarchy = 'date_creation'
    ordering = ('date_creation', )
    search_fields = ('string', 'used_by')

    def share_url(self, obj):
        return format_html('<a href="{url}" target="_blank">Link</a>', url=obj.share_url())


admin.site.register(Token, TokenAdmin)
