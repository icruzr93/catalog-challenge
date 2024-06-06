from rest_framework import serializers

from app.channel.models import Channel, ChannelPrice


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = (
            "id",
            "name",
            "description",
        )


class ChannelPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelPrice
        fields = (
            "channel_id",
            "product_id",
            "price",
        )
