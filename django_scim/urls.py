from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scim/v2/', include('slack_scim.urls')),
]