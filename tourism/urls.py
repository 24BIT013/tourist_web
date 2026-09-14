from django.urls import include, path

urlpatterns = [
    path('manage/', include('site_admin.urls')),
    path('', include('tour_app.urls')),
]
