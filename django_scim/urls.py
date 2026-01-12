from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/', views.api_home, name='api_home'),
    path('api/docs/', views.api_docs, name='api_docs'),
    path('scim/v2/', include('slack_scim.urls')),
]