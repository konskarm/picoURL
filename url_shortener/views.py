from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.response import Response

from .models import URLMapping
from .serializers import CreateURLMappingInputSerializer, URLStatsSerializer, CreateURLMappingOutputSerializer


class CreateURLMappingView(generics.CreateAPIView):
    """View that allows POST requests to create URL mappings."""
    serializer_class = CreateURLMappingInputSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateURLMappingInputSerializer(data=request.data)
        if serializer.is_valid():
            url_mapping = serializer.save()
            output_serializer = CreateURLMappingOutputSerializer(url_mapping)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def redirect_view(request, *args, **kwargs):
    obj = get_object_or_404(URLMapping, short_code=kwargs['short_code'])
    obj.times_used += 1
    obj.save()
    response = redirect(obj.original_url)
    return response


class UsageDetailsView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(URLMapping, short_code=kwargs['short_code'])
        serializer = URLStatsSerializer(obj)
        return Response(serializer.data)
