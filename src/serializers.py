from rest_framework import serializers


class CardUrlSerializer(serializers.Serializer):
    front_image_url = serializers.CharField()
    back_image_url = serializers.CharField()
    no_of_cards = serializers.IntegerField()
