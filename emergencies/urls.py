from django.urls import path
from .views import ReceiveEmergency, generate_hms_token

urlpatterns = [
    path('receive-emergency/', ReceiveEmergency.as_view(), name='receive-emergency'),
    path('hms-token/<str:report_id>/', generate_hms_token, name='hms-token'),
]