from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/packages/add/', views.package_create, name='package_create'),
    path('dashboard/packages/<int:pk>/edit/', views.package_edit, name='package_edit'),
    path('dashboard/packages/<int:pk>/delete/', views.package_delete, name='package_delete'),
]
