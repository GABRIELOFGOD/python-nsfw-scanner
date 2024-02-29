from rest_framework import serializers

class inputSerializer(serializers.Serializer):
    name = serializers.CharField()