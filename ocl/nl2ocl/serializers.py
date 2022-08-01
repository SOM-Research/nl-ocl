from rest_framework import serializers

class OCLTranslationSerializer(serializers.Serializer):
    translation = serializers.CharField(required=True)
