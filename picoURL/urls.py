from django.contrib import admin
from django.urls import path

from url_shortener.views import CreateURLMappingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CreateURLMappingView.as_view(), name="create"),
]
