from django.http import JsonResponse
from django.shortcuts import render, redirect

def home(request):
    # Redirect to login page - no direct access to home
    return redirect('/login/')

def login_view(request):
    return render(request, 'login.html')

def dashboard(request):
    # Protected home page - only accessible after login
    return render(request, 'home.html')

def user_management(request):
    return render(request, 'user_management.html')

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