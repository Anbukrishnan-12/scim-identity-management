from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Redirects to login
    path('login/', views.login_view, name='login'),
    path('home/', views.dashboard, name='dashboard'),  # Protected home page
    path('manage/', views.user_management, name='user_management'),
    path('api/', views.api_home, name='api_home'),
    path('api/docs/', views.api_docs, name='api_docs'),
    path('scim/v2/', include('slack_scim.urls')),
]