from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Invitation
from .forms import invitationAdminForm

class SentFilter(admin.SimpleListFilter):
    title = _('Sent')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'sent'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. (value, label)
        """
        return (
            ('true', _('Yes')),
            ('false', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(sent_to__isnull=False)
        if self.value() == 'false':
            return queryset.filter(sent_to__isnull=True)

class InvitationAdmin(admin.ModelAdmin):
    form = invitationAdminForm
    list_display = (
        'token_trim',
        'date_creation',
        'nb_libraries',
        'sent_to',
        'date_usage',
        'used_by',
        'share_url')
    list_filter = (
        'date_usage',
        SentFilter)
    date_hierarchy = 'date_creation'
    ordering = ('date_creation', )
    search_fields = ('token', 'used_by')
    readonly_fields = ('date_usage', 'used_by')

    def token_trim(self, obj: Invitation):
        return format_html('<div class="token-hash" title="{token}">{token}</div>', token=obj.token)
    token_trim.short_description = _('Token')
    token_trim.admin_order_field = 'token'

    def share_url(self, obj: Invitation):
        return format_html('<a href="{url}" target="_blank">{link}</a>', url=obj.share_url(), link=_('Link'))
    share_url.short_description = _('Url')

    def mark_not_sent(self, request, queryset):
        queryset.update(sent_to = None)
    mark_not_sent.short_description = _('Mark as not sent')

    actions = (mark_not_sent, )

    class Media:
        css = {
            'all': ('plex/css/admin.css',)
        }

admin.site.register(Invitation, InvitationAdmin)

admin.site.site_header = _('Plexoffice admin')
admin.site.site_title = _('Plexoffice admin')
admin.site.index_title = _('Plexoffice administration')
