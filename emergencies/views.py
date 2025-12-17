from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Emergency

class ReceiveEmergency(APIView):
    def post(self, request):
        data = request.data

        # Prevent duplicates
        if Emergency.objects.filter(emergency_id=data.get('reportId')).exists():
            return Response({"message": "Already exists"}, status=status.HTTP_200_OK)

        Emergency.objects.create(
            emergency_id=data.get('reportId'),
            type=data.get('type'),
            location=data.get('location'),
            details=data.get('details', ''),
            urgency=data.get('urgency', 'medium'),
            contact_method=data.get('contactMethod', 'both'),
            additional_info=data.get('additionalInfo', {}),
            created_by_uid=data.get('createdByUID'),
            display_code=data.get('displayCode', 'ANON'),
            status='pending',
        )

        return Response({"message": "Emergency received"}, status=status.HTTP_201_CREATED)