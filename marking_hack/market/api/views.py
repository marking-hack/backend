from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from marking_hack.common.api import BigResultsSetPagination
from marking_hack.market.api.serializers import (
    StoreSerializer,
    ItemSerializer,
    ListRegionSerializer,
    ItemSaleSerializer,
    ItemTransactionSerializer,
    PredictSerializer,
)
from marking_hack.market.models import Store, Region, StoreItem, Item


class ListStore(generics.ListAPIView):
    serializer_class = StoreSerializer
    pagination_class = BigResultsSetPagination
    queryset = Store.objects.order_by("-id_sp")


class ListStoreItems(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = BigResultsSetPagination

    def get_queryset(self):
        store = get_object_or_404(Store, id_sp=self.kwargs["id_sp"])
        ids = (
            StoreItem.objects.filter(store=store)
            .values_list("item", flat=True)
            .distinct()
        )
        return Item.objects.filter(id__in=ids)


class RegionListView(generics.ListAPIView):
    serializer_class = ListRegionSerializer
    queryset = Region.objects.all()


class RegionSalesListView(generics.ListAPIView):
    serializer_class = ItemSaleSerializer

    def get_queryset(self):
        region = get_object_or_404(Region, code=self.kwargs["code"])
        return region.sales.all()


class RegionTransactionsListView(generics.ListAPIView):
    serializer_class = ItemTransactionSerializer

    def get_queryset(self):
        region = get_object_or_404(Region, code=self.kwargs["code"])
        return region.transactions.all()


class PredictItemsView(generics.GenericAPIView):
    serializer_class = PredictSerializer

    def post(self, request, *args, **kwargs):
        serializer = PredictSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        shops = [dict(x) for x in data["shops"]]
        for shop in shops:
            store = get_object_or_404(Store, id_sp=shop["id_sp"])
            items = []
            for x_item in shop["items"]:
                item = get_object_or_404(Item, gtin=x_item)
                qs = StoreItem.objects.filter(store=store, item=item)
                if qs.exists():
                    items.append({"id": x_item, "predicted_volume": qs.last().amount})
                else:
                    print(qs)
                    items.append({"id": x_item, "predicted_volume": 0})
        data["shops"] = shops
        return Response(data=data)
