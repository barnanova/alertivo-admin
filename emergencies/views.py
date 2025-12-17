from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Emergency

class ReceiveEmergency(APIView):
    def post(self, request):
        data = request.data

        report_id = data.get('reportId')
        if not report_id:
            return Response({"error": "reportId is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicates
        if Emergency.objects.filter(emergency_id=report_id).exists():
            return Response({"message": "Already exists"}, status=status.HTTP_200_OK)

        # Whitelist only allowed fields — this prevents any unexpected fields like 'additional_info'
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