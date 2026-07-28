from django.contrib import admin
from django.utils.html import format_html
from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role_badge', 'phone', 'email', 'status_badge', 'hire_date', 'commission_rate']
    list_filter = ['role', 'status', 'salon']
    search_fields = ['full_name', 'phone', 'email']
    ordering = ['full_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Personal Info', {
            'fields': ('salon', 'user', 'full_name', 'phone', 'email'),
        }),
        ('Employment', {
            'fields': ('role', 'status', 'hire_date', 'commission_rate'),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def role_badge(self, obj):
        colors = {
            'stylist': '#6c63ff', 'colorist': '#e91e63', 'nail_tech': '#ff9800',
            'aesthetician': '#4caf50', 'manager': '#2196f3',
            'receptionist': '#009688', 'other': '#9e9e9e',
        }
        color = colors.get(obj.role, '#9e9e9e')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:12px;font-size:11px">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Role'

    def status_badge(self, obj):
        colors = {'active': '#4caf50', 'inactive': '#f44336', 'on_leave': '#ff9800'}
        color = colors.get(obj.status, '#9e9e9e')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:12px;font-size:11px">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
