from django.urls import path
from .views import ReceiveEmergency

urlpatterns = [
    path('receive-emergency/', ReceiveEmergency.as_view(), name='receive-emergency'),
]