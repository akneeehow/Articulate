from django.urls import path
from . import views



urlpatterns = [
    path('visit/<str:username>/', views.user_profile_view, name='user_profile'),
    path('verify_email/<str:username>/', views.verify_email, name='verify_email'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('avatar_upload/<str:username>/', views.avatar_upload, name="avatar_upload"),
    path('edit/<str:username>/', views.edit_profile, name='edit_profile'),
]
