from rest_framework import serializers
from .models import Furniture

class FurnitureSerializer(serializers.ModelSerializer):
    model_url = serializers.ReadOnlyField(source='firebase_model_url')
    thumbnail_url = serializers.ReadOnlyField(source='firebase_thumbnail_url')

    class Meta:
        model = Furniture
        fields = ['id', 'name', 'model_url', 'thumbnail_url', 'created_at']