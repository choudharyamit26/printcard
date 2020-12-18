from django.urls import path
from .views import CreatePdf

from django.conf import settings
from django.conf.urls.static import static

app_name = 'src'

urlpatterns = [
    path('', CreatePdf.as_view(), name='pdf')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
