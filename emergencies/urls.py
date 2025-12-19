from django.urls import path
from .views import ReceiveEmergency
from .views import generate_agora_token

urlpatterns = [
    path('receive-emergency/', ReceiveEmergency.as_view(), name='receive-emergency'),
    path('agora-token/<str:report_id>/', generate_agora_token, name='agora-token'),
]