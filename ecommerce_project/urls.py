from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL for Django admin interface
    path('', include('store.urls')),  # Include URLs from the 'store' app
]
