from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Emergency
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import time

# Existing API for receiving emergencies from the app
class ReceiveEmergency(APIView):
    def post(self, request):
        data = request.data

        report_id = data.get('reportId')
        if not report_id:
            return Response({"error": "reportId is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicates
        if Emergency.objects.filter(emergency_id=report_id).exists():
            return Response({"message": "Already exists"}, status=status.HTTP_200_OK)

        # Whitelist only allowed fields — safe from extra data
        allowed_data = {
            'emergency_id': report_id,
            'type': data.get('type', 'medical'),
            'location': data.get('location', {}),
            'details': data.get('details', {}),
            'notes': data.get('notes', ''),
            'urgency': data.get('urgency', 'medium'),
            'contact_method': data.get('contactMethod', 'both'),
            'created_by_uid': data.get('createdByUID', ''),
            'display_code': data.get('displayCode', 'ANON'),
            'status': 'pending',
        }

        try:
            Emergency.objects.create(**allowed_data)
            return Response({"message": "Emergency received"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# New: Generate Agora token for VoIP call
def generate_agora_token(request, report_id):
    # Replace with your actual Agora credentials
    app_id = "e47007b648fb4f65ba065f0b337c418d"
    app_certificate = "b6dc0a6f2c71405d81e7ad7284a935ba"

    uid = 0  # 0 means Agora assigns UID automatically
    role = 1  # 1 = Broadcaster (can publish audio)
    expiration_time_in_seconds = 3600  # 1 hour
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(
        app_id, app_certificate, report_id, uid, role, privilege_expired_ts
    )

    return JsonResponse({
        'token': token,
        'appId': app_id
    })