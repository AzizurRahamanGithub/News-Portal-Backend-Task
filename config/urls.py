from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse, HttpResponse
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home

def favicon(request):
    return HttpResponse(status=204)

# URL Patterns
urlpatterns = [
    path("", home),  
    re_path(r'^favicon.ico$', favicon), 
    path('admin/', admin.site.urls), 
    path('summernote/', include('django_summernote.urls')),
    path('nested_admin/', include('nested_admin.urls')),
    
    path('api/v1/', include([
        path('schema-viewer/', include('schema_viewer.urls')),
        path('auth/', include('apps.auths.urls')),
        path('file/', include('apps.file_uploader.urls')),
        path('notification/', include('apps.notification.urls')),
        path('news/', include('apps.multicontent.urls')),
        
    ])),
]

# Static files for development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
