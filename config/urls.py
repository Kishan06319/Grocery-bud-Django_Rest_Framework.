from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import TemplateView

# This creates a simple message when you visit the root URL so you know it works
def api_home(request):
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Your Grocery API Routes
    path('api/grocery/', include('grocery.urls')),

    # Serve React frontend
    path('', TemplateView.as_view(template_name='index.html'), name='frontend'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)