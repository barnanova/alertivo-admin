from django.contrib import admin
from django.utils.html import format_html
from .models import Emergency

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('emergency_id', 'type', 'urgency', 'status', 'created_at', 'display_code', 'join_call_button')
    list_filter = ('type', 'status', 'urgency', 'created_at')
    search_fields = ('emergency_id', 'notes', 'created_by_uid', 'display_code')
    readonly_fields = ('created_at', 'emergency_id', 'medical_details', 'join_call_button')

    fieldsets = (
        ('Emergency Overview', {
            'fields': ('emergency_id', 'type', 'status', 'urgency', 'contact_method', 'display_code')
        }),
        ('Location', {
            'fields': ('location',),
        }),
        ('Medical Summary', {
            'fields': ('medical_details',),
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
        ('Communication', {
            'fields': ('join_call_button',),
            'description': 'Staff can join the call only after the student initiates it'
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

    # Staff "Join VoIP Call" button
    def join_call_button(self, obj):
        if obj.contact_method in ['call', 'both']:
            return format_html(
                '<button type="button" onclick="joinAgoraCall(\'{}\')" '
                'style="background:#E63946;color:white;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-weight:bold;font-size:14px;">'
                '📞 Join VoIP Call</button>'
                '<script src="https://download.agora.io/sdk/release/AgoraRTC_N-4.20.1.js"></script>'
                '<script>'
                'async function joinAgoraCall(channel) {{'
                '  try {{'
                '    const res = await fetch(`/api/agora-token/${{channel}}/`);'
                '    if (!res.ok) throw new Error("Token error");'
                '    const data = await res.json();'
                '    const client = AgoraRTC.createClient({{mode:"rtc", codec:"vp8"}});'
                '    await client.join(data.appId, channel, data.token, null);'
                '    const mic = AgoraRTC.createMicrophoneAudioTrack();'
                '    await client.publish([mic]);'
                '    alert("You have joined the call — speak to the student now");'
                '  }} catch (err) {{'
                '    alert("Failed to join call: " + err.message);'
                '  }}'
                '}}'
                '</script>',
                obj.emergency_id
            )
        return format_html('<span style="color:#888;">Call not available (student preference: chat only)</span>')
    join_call_button.short_description = "VoIP Call"
    join_call_button.allow_tags = True