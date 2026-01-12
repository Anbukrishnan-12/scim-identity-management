from django.urls import path
from . import views

app_name = 'slack_scim'

urlpatterns = [
    # SCIM Users endpoints
    path('Users/', views.user_list, name='user-list'),
    path('Users/<str:user_id>/', views.user_detail, name='user-detail'),
]