from django.db import models

class Emergency(models.Model):
    TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('fire', 'Fire'),
        ('security', 'Security'),
    ]

    CONTACT_CHOICES = [
        ('chat', 'Chat Only'),
        ('call', 'Call Only'),
        ('both', 'Both'),
    ]

    emergency_id = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.JSONField()  # {readableAddress, lat, lng}
    details = models.JSONField(null=True, blank=True)  # Medical: {who, medType, numAffected, urgency}
    notes = models.TextField(blank=True)  # Free text description
    urgency = models.CharField(max_length=20, blank=True)
    contact_method = models.CharField(max_length=10, choices=CONTACT_CHOICES, default='both')
    created_by_uid = models.CharField(max_length=100, blank=True)
    display_code = models.CharField(max_length=20, default='ANON')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.emergency_id}"

    def medical_details(self):
        if self.type != 'medical' or not self.details:
            return "N/A"
        d = self.details
        return f"Affected: {d.get('who', 'N/A')} | Type: {d.get('medType', 'N/A')} | Number: {d.get('numAffected', 'N/A')} | Urgency: {d.get('urgency', 'N/A')}"