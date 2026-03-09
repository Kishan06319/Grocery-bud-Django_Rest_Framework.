from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
import os
import logging

logger = logging.getLogger(__name__)

def api_home(request):
    logger.info("API home endpoint called")
    return JsonResponse({
        "status": "success",
        "message": "Django Backend API is running perfectly!"
    })

def serve_react(request):
    """Serve React index.html for SPA routing"""
    logger.info(f"Serving React app for path: {request.path}")
    logger.info(f"BASE_DIR: {settings.BASE_DIR}")

    # Try multiple possible paths for the dist directory
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'grocery-bud-react', 'dist', 'index.html'),
        os.path.join(settings.BASE_DIR, '..', 'grocery-bud-react', 'dist', 'index.html'),
        '/opt/render/project/src/grocery-bud-react/dist/index.html',
        '/app/grocery-bud-react/dist/index.html',
    ]

    for index_file in possible_paths:
        logger.info(f"Checking path: {index_file}")
        if os.path.exists(index_file):
            logger.info(f"Found index.html at: {index_file}")
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logger.info(f"Successfully read {len(content)} characters")
                    return HttpResponse(content, content_type='text/html')
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                continue

    logger.error("Frontend not found in any expected location")
    logger.error(f"Tried paths: {possible_paths}")

    # Return a simple HTML page for debugging
    debug_info = f"""
    <h1>Frontend Not Found</h1>
    <p>BASE_DIR: {settings.BASE_DIR}</p>
    <p>Current working directory: {os.getcwd()}</p>
    <p>Tried paths:</p>
    <ul>
    """

    for path in possible_paths:
        exists = os.path.exists(path)
        debug_info += f"<li>{path} - {'EXISTS' if exists else 'NOT FOUND'}</li>"

    debug_info += "</ul>"

    return HttpResponse(debug_info, content_type='text/html', status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/grocery/', include('grocery.urls')),
    re_path(r'^(?!api|admin|static)', serve_react),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)