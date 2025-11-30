from django.contrib import admin
from django.urls import include, path
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', main_views.CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
