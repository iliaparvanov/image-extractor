# todos/serializers.py
from rest_framework import serializers
from .models import Image

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return value.tobytes().decode('utf-8')

    def to_internal_value(self, value):
        return value.tobytes().encode('utf-8')

class ImageSerializer(serializers.ModelSerializer):
    hash = BinaryField()

    class Meta:
        model = Image
        fields = ('id', 'url', 'hash', 'width', 'height', 'type')

class ImageCreationSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)