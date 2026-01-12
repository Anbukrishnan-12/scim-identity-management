from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def api_home(request):
    return JsonResponse({
        "message": "SCIM Identity Management System",
        "version": "2.0",
        "endpoints": {
            "users": "/scim/v2/Users/",
            "user_detail": "/scim/v2/Users/{id}/",
            "documentation": "/api/docs/"
        },
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
        "status": "API Server Running"
    })

def api_docs(request):
    return render(request, 'api_docs.html')