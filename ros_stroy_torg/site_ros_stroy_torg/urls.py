from django.urls import path
from .views import order_summary, order_success
from django.conf import settings
from django.conf.urls.static import static


app_name = 'site_ros_stroy_torg'

urlpatterns = [
    path('order_summary/',order_summary, name = 'order_summary'),
    path('order_success/', order_success, name='order_success'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)