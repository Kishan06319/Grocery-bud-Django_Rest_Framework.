from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
import os

def api_home(request):
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

def serve_react(request):
    """Serve React index.html for SPA routing"""
    dist_dir = os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist')
    index_file = os.path.join(dist_dir, 'index.html')
    
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    
    return HttpResponse(
        "<h1>Error: Frontend not built</h1><p>Run: npm run build in grocery-bud-react/</p>",
        content_type='text/html',
        status=500
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/grocery/', include('grocery.urls')),
    re_path(r'^(?!api|admin|static)', serve_react),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)