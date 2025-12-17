from django.contrib import admin
from .models import Emergency

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('emergency_id', 'type', 'urgency', 'status', 'created_at', 'display_code')
    list_filter = ('type', 'status', 'urgency', 'created_at')
    search_fields = ('emergency_id', 'notes', 'created_by_uid', 'display_code')
    readonly_fields = ('created_at', 'emergency_id', 'medical_details')  # ← Add medical_details here

    fieldsets = (
        ('Emergency Overview', {
            'fields': ('emergency_id', 'type', 'status', 'urgency', 'contact_method', 'display_code')
        }),
        ('Location', {
            'fields': ('location',),
        }),
        ('Medical Summary', {
            'fields': ('medical_details',),  # ← Show the method output here
            'description': 'Auto-generated summary for medical emergencies'
        }),
        ('Details (JSON)', {
            'fields': ('details',),
            'description': 'Raw medical details object'
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
        if obj.type != 'medical':
            return "N/A (not a medical emergency)"
        d = obj.details or {}
        return f"Affected: {d.get('who', 'N/A')} | Type: {d.get('medType', 'N/A')} | Number: {d.get('numAffected', 'N/A')} | Urgency: {d.get('urgency', 'N/A')}"
    medical_details.short_description = "Medical Summary"