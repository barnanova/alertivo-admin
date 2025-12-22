from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Emergency
from django.http import JsonResponse
import jwt
import uuid
import time
import os

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

# 100ms token generation (using PyJWT — official method)
def generate_hms_token(request, report_id):
    # Get secrets from environment variables (set in Render dashboard)
    app_access_key = os.environ.get('HMS_APP_ACCESS_KEY')
    app_secret = os.environ.get('HMS_APP_SECRET')

    if not app_access_key or not app_secret:
        return JsonResponse({"error": "Server configuration error"}, status=500)

    payload = {
        "access_key": app_access_key,
        "room_id": report_id,
        "user_id": str(uuid.uuid4()),  # Unique per session
        "role": "guest",  # Change to "host" for staff if needed
        "type": "app",
        "version": 2,
        "iat": int(time.time()),
        "nbf": int(time.time()),
        "exp": int(time.time()) + 3600,  # 1 hour
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(payload, app_secret, algorithm="HS256")

    return JsonResponse({"token": token})