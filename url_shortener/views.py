from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import CreateURLMappingInputSerializer, CreateURLMappingOutputSerializer


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
