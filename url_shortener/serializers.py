from rest_framework import serializers, status
from rest_framework.response import Response

from utils.config import CONFIG
from utils.hasher import URLHasher
from .models import URLMapping


class CreateURLMappingSerializer(serializers.ModelSerializer):
    """
    Serializer to map the model instance to json format. Intended for use as the input
    serializer in the create view.
    """

    class Meta:
        """Map the serializer to the model, exposing only the original_url field."""
        model = URLMapping
        fields = ('original_url', 'short_code',)
        read_only_fields = ('short_code',)

    def create(self, validated_data):
        """
        Overrides the create method to include the hashing process of the , before storing it
        to the database.
        """
        url = validated_data['original_url']
        url_hasher = URLHasher()
        short_code = url_hasher.hash(url)

        # Rehash the url if it collides with an existing short_code.
        # To avoid the infinite loop, we will rehash up to a maximum number of times.
        retries = 0
        while URLMapping.objects.filter(short_code=short_code).exists():
            short_code = url_hasher.rehash()
            retries += 1
            if retries > CONFIG.MAX_HASHING_RETRIES:
                response_error = "Failed to find a unique hash after {} retries.".format(CONFIG.MAX_HASHING_RETRIES)
                # TODO We could specify a specific 5xx error in this case instead of using the generic one
                return Response({"Fail": response_error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return URLMapping.objects.create(
            short_code=short_code,
            **validated_data
        )


class URLStatsSerializer(serializers.ModelSerializer):
    """Serializer to map the model instance into json format for the stats view."""

    class Meta:
        """Map the serializer to the model, exposing the stats fields."""
        model = URLMapping
        fields = ('original_url', 'creation_date', 'times_used')
