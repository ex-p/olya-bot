from django.conf import settings
from django.contrib import admin
from django.urls import path

from olya import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/{}'.format(settings.CALLBACK_PATH), views.callback),
    path('', views.index)
]
