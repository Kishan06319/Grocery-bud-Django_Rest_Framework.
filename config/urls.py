from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, FileResponse
from django.views.generic import TemplateView
import os

# This creates a simple message when you visit the root URL so you know it works
def api_home(request):
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

def serve_react(request):
    """Serve the React app's index.html file"""
    index_path = os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist', 'index.html')
    try:
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    except FileNotFoundError:
        return JsonResponse({"error": "Frontend not found"}, status=404)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Your Grocery API Routes
    path('api/grocery/', include('grocery.urls')),

    # Serve React frontend
    path('', serve_react, name='frontend'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)