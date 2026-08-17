from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.admin_dashboard import custom_admin_site

# Register admin site URLs
admin.autodiscover()

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('django-admin/', admin.site.urls),  # Original admin for superusers
    path('accounts/', include('django.contrib.auth.urls')),  # Django built-in auth URLs
    path('', include('core.urls')),
    path('doctors/', include('doctors.urls')),
    path('patients/', include('patients.urls')),
    path('booking/', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)