from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.response import Response

from .models import URLMapping
from .serializers import CreateURLMappingSerializer, URLStatsSerializer


class CreateURLMappingView(generics.CreateAPIView):
    """View that allows POST requests to create URL mappings."""

    serializer_class = CreateURLMappingSerializer


def redirect_view(request, *args, **kwargs):
    obj = get_object_or_404(URLMapping, short_code=kwargs['short_code'])
    obj.times_used += 1
    obj.save()
    return redirect(obj.original_url)


class UsageDetailsView(generics.RetrieveAPIView):
    # maybe

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(URLMapping, short_code=kwargs['short_code'])
        serializer = URLStatsSerializer(obj)
        return Response(serializer.data)
