from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.static import serve as serve_static
import os

# This creates a simple message when you visit the root URL so you know it works
def api_home(request):
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

def serve_react(request):
    """Serve the React app's index.html file"""
    dist_path = os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist')
    index_path = os.path.join(dist_path, 'index.html')
    
    if os.path.exists(index_path):
        return serve_static(request, 'index.html', document_root=dist_path)
    else:
        return JsonResponse({"error": f"Frontend not found at {dist_path}"}, status=404)

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