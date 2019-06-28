from django.contrib import admin
from django.utils.html import format_html
from .models import Invitation
from .forms import invitationAdminForm


class InvitationAdmin(admin.ModelAdmin):
    form = invitationAdminForm
    list_display = (
        'token_hash',
        'date_creation',
        'nb_libraries',
        'sent_to',
        'date_usage',
        'used_by',
        'share_url')
    list_filter = (
        'date_usage',)
    date_hierarchy = 'date_creation'
    ordering = ('date_creation', )
    search_fields = ('token', 'used_by')
    readonly_fields = ('date_usage', 'used_by', 'share_url')

    def token_hash(self, obj):
        return format_html('<div class="token-hash" title="{token}">{token}</div>', token=obj.token)

    def share_url(self, obj):
        return format_html('<a href="{url}" target="_blank">Link</a>', url=obj.share_url())

    def mark_sent(self, request, queryset):
        queryset.update(sent = True)
    mark_sent.short_description = "Marquer comme envoyées"

    def mark_not_sent(self, request, queryset):
        queryset.update(sent = False)
    mark_not_sent.short_description = "Marquer comme NON envoyées"

    actions = (mark_sent, mark_not_sent)

    class Media:
        css = {
            'all': ('plex/css/admin.css',)
        }


admin.site.register(Invitation, InvitationAdmin)

admin.site.site_header = 'Plexoffice admin'
admin.site.site_title = 'Plexoffice admin'
admin.site.index_title = 'Plexoffice administration'
