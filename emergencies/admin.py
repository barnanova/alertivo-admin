from django.contrib import admin
from .models import Emergency

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('emergency_id', 'type', 'urgency', 'status', 'created_at', 'display_code')
    list_filter = ('type', 'status', 'urgency', 'created_at')
    search_fields = ('emergency_id', 'notes', 'created_by_uid', 'display_code')
    readonly_fields = ('created_at', 'emergency_id')

    fieldsets = (
        ('Emergency Overview', {
            'fields': ('emergency_id', 'type', 'status', 'urgency', 'contact_method', 'display_code')
        }),
        ('Location', {
            'fields': ('location',),
        }),
        ('Medical Details (if applicable)', {
            'fields': ('medical_details', 'details'),
            'description': 'Only shown for medical emergencies'
        }),
        ('Description', {
            'fields': ('notes',),
        }),
        ('Student Info', {
            'fields': ('created_by_uid',),
        }),
        ('Timestamp', {
            'fields': ('created_at',),
        }),
    )

    def medical_details(self, obj):
        return obj.medical_details()
    medical_details.short_description = "Medical Summary"