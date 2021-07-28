# imports
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from start3.nbb.views import Index
# End: imports -----------------------------------------------------------------

urlpatterns = [
    path('', Index.as_view(), name="index"), # TODO Replace startsite
    path('start3/', include('start3.main.urls')),
    path('brukere/', include('accounts.urls')),
    path('acl/accounts/', include('accounts.urls_acl')),
    path('admin/django/', admin.site.urls, name="admin"),
]

urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
