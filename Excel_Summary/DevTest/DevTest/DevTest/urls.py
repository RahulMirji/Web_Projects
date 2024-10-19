from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('file_upload.urls')),  # <-- Include the app's URLs
]
