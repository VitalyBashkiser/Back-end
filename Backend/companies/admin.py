from django.contrib import admin
from .models import Company, Invitation, Request


def toggle_visibility(modeladmin, request, queryset):
    queryset.update(is_visible=not queryset.first().is_visible)


toggle_visibility.short_description = "Toggle Visibility"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'is_visible', 'owner')
    list_filter = ('owner', 'is_visible')
    search_fields = ('name', 'description')
    actions = [toggle_visibility]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Request)
admin.site.register(Invitation)