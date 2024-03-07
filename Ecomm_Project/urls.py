from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from administrator import views as admin_views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('authentication/',include('authentication.urls')),
    path('administrator/',include('administrator.urls')),
    path('',admin_views.homepage,name='home'),
    path('verification/', include('verify_email.urls')),	
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
