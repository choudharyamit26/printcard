from rest_framework import serializers


class CardUrlSerializer(serializers.Serializer):
    front_image_url = serializers.CharField()
    # front_image_url = serializers.ImageField()
    back_image_url = serializers.CharField()
    # back_image_url = serializers.ImageField()
    no_of_cards = serializers.IntegerField()


class CreateBrochureOrLetterHeadSerializer(serializers.Serializer):
    front_image_url = serializers.CharField()
    back_image_url = serializers.CharField()
    page_count = serializers.IntegerField()
