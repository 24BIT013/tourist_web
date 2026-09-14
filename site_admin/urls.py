from django.urls import path

from . import views

app_name = 'site_admin'

urlpatterns = [
    path('login/', views.ManagementLoginView.as_view(), name='login'),
    path('logout/', views.management_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('<slug:section>/add/', views.record_create, name='record_create'),
    path('<slug:section>/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('<slug:section>/<int:pk>/delete/', views.record_delete, name='record_delete'),
]
