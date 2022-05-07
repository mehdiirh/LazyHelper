from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from control import urls as control_urls
from api import urls as api_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(control_urls)),
    path('api/', include(api_urls)),

] + static('/cdn/', document_root=settings.MEDIA_ROOT)


admin.site.site_header = '🦥 Lazy Helper'
admin.site.site_title = '🦥 Lazy Helper'
admin.site.index_title = 'Control Panel'
