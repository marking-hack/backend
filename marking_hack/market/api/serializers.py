from numpy import nan
from rest_framework import serializers

from marking_hack.market.models import Store, Region, Item, ItemSale, ItemTransaction


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id_sp", "region_name", "city_name", "postal_code"]


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product_name")
    category = serializers.CharField(source="product_short_name")
    current_amount = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    def get_current_amount(self, obj):
        amount = obj.sales.first().amount
        if amount == nan:
            return 0
        try:
            return int(amount)
        except ValueError:
            return 0

    def get_volume(self, obj):
        if obj.volume == nan:
            return 0
        try:
            return int(obj.volume)
        except ValueError:
            return 0

    class Meta:
        model = Item
        fields = [
            "gtin",
            "name",
            "category",
            "brand",
            "country",
            "volume",
            "current_amount",
        ]


class ListRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["code", "name"]


class ItemSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSale
        fields = ["date", "type_operation", "cnt"]


class ItemTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTransaction
        fields = ["date", "cnt", "sender_region_code"]


class ShopItemSerializer(serializers.Serializer):
    id_sp = serializers.CharField(max_length=32)
    items = serializers.ListSerializer(child=serializers.CharField(max_length=32))


class PredictSerializer(serializers.Serializer):
    date = serializers.DateField()
    shops = ShopItemSerializer(many=True)
