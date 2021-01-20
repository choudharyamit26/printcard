from django.urls import path
from .views import CreatePdf, CreateBrochureOrLetterHead, CreatePdfViewSet

from django.conf import settings
from django.conf.urls.static import static

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'pdf', CreatePdfViewSet, basename='pdf')
# urlpatterns = router.urls
app_name = 'src'

urlpatterns = [
    path('', CreatePdf.as_view(), name='pdf'),
    path('brochure-or-letter-head/', CreateBrochureOrLetterHead.as_view(), name='pdf')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
