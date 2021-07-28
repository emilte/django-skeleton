# imports
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from root import views as root_views
# End: imports -----------------------------------------------------------------

urlpatterns = [
    # path('', Index.as_view(), name="index"), # TODO Replace startsite
    path('admin/', admin.site.urls, name="admin"),
]

urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
