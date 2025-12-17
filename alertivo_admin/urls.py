from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

admin.site.site_header = "AlertivoHealth Admin"
admin.site.site_title = "AlertivoHealth"
admin.site.index_title = "AlertivoHealth Dashboard"

def redirect_to_admin(request):
    return redirect('admin:index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('emergencies.urls')),  # Better: group API under /api/
    path('', redirect_to_admin),  # Root → admin
]