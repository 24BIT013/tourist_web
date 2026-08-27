from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    # Keep ID-based links working while public links use readable slugs.
    # This route must precede the slug route because a numeric ID is also a
    # valid slug.
    path('packages/<int:pk>/', views.package_detail_by_id, name='package_detail_by_id'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/packages/add/', views.package_create, name='package_create'),
    path('dashboard/packages/<int:pk>/edit/', views.package_edit, name='package_edit'),
    path('dashboard/packages/<int:pk>/delete/', views.package_delete, name='package_delete'),
    path('dashboard/destinations/add/', views.destination_create, name='destination_create'),
    path('dashboard/destinations/<int:pk>/edit/', views.destination_edit, name='destination_edit'),
]
