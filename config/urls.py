from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.static import serve as serve_static
from django.views.decorators.cache import cache_page
import os

# This creates a simple message when you visit the root URL so you know it works
def api_home(request):
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

def get_index_html():
    """Get the index.html content with multiple fallback paths"""
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist', 'index.html'),
        os.path.join(settings.BASE_DIR, '..', 'grocery-bud-react', 'dist', 'index.html'),
        '/app/grocery-bud-react/dist/index.html',
        '/opt/render/project/src/grocery-bud-react/dist/index.html',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                continue
    return None

def serve_react(request):
    """Serve the React app's index.html file for SPA routing"""
    index_content = get_index_html()
    
    if index_content:
        return HttpResponse(index_content, content_type='text/html')
    else:
        return HttpResponse(
            "<h1>Frontend not found</h1><p>Please ensure React has been built.</p>",
            content_type='text/html',
            status=500
        )

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Your Grocery API Routes
    path('api/grocery/', include('grocery.urls')),

    # Catch-all for React SPA - must be last
    re_path(r'^(?!api|admin).*', serve_react, name='frontend'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)