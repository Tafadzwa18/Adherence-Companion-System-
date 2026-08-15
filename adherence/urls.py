
from django.urls import path
from django.contrib.auth import views as auth_views
from django import views


urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='adherence/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Medication CRUD
    path('medications/', views.MedicationListView.as_view(), name='medication-list'),
    path('medications/add/', views.MedicationCreateView.as_view(), name='medication-add'),
    
    # Adherence Logs
    path('logs/add/', views.AdherenceLogCreateView.as_view(), name='log-add'),
]
