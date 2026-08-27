from django.contrib import admin

from comunicaciones.models import Communication


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'pinned')
    list_filter = ('pinned',)
