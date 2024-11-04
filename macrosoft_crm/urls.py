# macrosoft_crm/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin Routes
    path('admin/', admin.site.urls),

    # Admin Panel App Routes
    path('', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),

    # API Routes
    path('api/', include('admin_panel.urls')),

    # Swagger and Redoc Documentation Routes
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Optional: Custom Permission Denied Handler
# Uncomment and customize the following line if you have a custom 403 handler
# handler403 = 'admin_panel.views.permission_denied_view'