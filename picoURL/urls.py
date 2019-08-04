from django.contrib import admin
from django.urls import path, re_path

from url_shortener.views import CreateURLMappingView, redirect_view, UsageDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CreateURLMappingView.as_view(), name='create'),
    re_path(r'^(?P<short_code>[a-zA-Z0-9_-]*)/$', redirect_view, name='redirect'),
    re_path(r'^(?P<short_code>[a-zA-Z0-9_-]*)/stats/$', UsageDetailsView.as_view(), name='short-code-stats'),
]
