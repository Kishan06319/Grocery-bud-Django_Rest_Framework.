import os

from django.http import JsonResponse
from django.shortcuts import redirect


def home(request):
    frontend_url = os.getenv("FRONTEND_URL", "").strip()
    if frontend_url:
        return redirect(frontend_url)
    return redirect("grocery:grocery-list")


def health(request):
    return JsonResponse({"status": "ok"})
