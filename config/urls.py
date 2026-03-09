from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.static import serve as serve_static
import os
import logging

logger = logging.getLogger(__name__)

def serve_static_assets(request, path):
    """Serve static assets from the dist folder"""
    dist_dir = os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist')
    full_path = os.path.join(dist_dir, path)
    
    # Security check - prevent directory traversal
    if not os.path.abspath(full_path).startswith(os.path.abspath(dist_dir)):
        return HttpResponse("Forbidden", status=403)
    
    if os.path.isfile(full_path):
        logger.info(f"Serving asset: {path}")
        return serve_static(request, path, document_root=dist_dir)
    
    return HttpResponse("Not Found", status=404)

def api_home(request):
    logger.info("API home endpoint called")
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

def serve_react(request):
    """Serve React index.html for SPA routing"""
    logger.info(f"Serving React app for path: {request.path}")
    dist_dir = os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist')
    index_file = os.path.join(dist_dir, 'index.html')
    
    if os.path.exists(index_file):
        logger.info(f"Found index.html at: {index_file}")
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"Successfully read {len(content)} characters")
                return HttpResponse(content, content_type='text/html')
        except Exception as e:
            logger.error(f"Error reading index.html: {e}")
            return HttpResponse(f"Error: {e}", content_type='text/html', status=500)
    
    logger.error(f"Frontend not found at {dist_dir}")
    return HttpResponse(
        f"<h1>Frontend Not Found</h1><p>Expected: {index_file}</p>",
        content_type='text/html',
        status=500
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/grocery/', include('grocery.urls')),
    # Serve static assets from dist folder BEFORE the catch-all
    re_path(r'^assets/(?P<path>.*)$', serve_static_assets, name='serve_dist_assets'),
    re_path(r'^.*\.(?:js|css|svg|png|jpg|jpeg|gif|woff|woff2|ttf|eot)$', serve_static_assets, name='serve_assets_by_extension'),
    # Catch-all for React SPA - serve index.html for all other routes
    re_path(r'^.*$', serve_react),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)