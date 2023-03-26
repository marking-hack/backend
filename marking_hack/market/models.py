import uuid

from django.db import models


class Region(models.Model):
    code = models.IntegerField(unique=True, primary_key=True, db_index=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    fias = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    name = models.CharField(max_length=250)


class Store(models.Model):
    id_sp = models.CharField(max_length=32, unique=True, db_index=True)
    member = models.ForeignKey(
        "Member", related_name="stores", on_delete=models.CASCADE
    )
    region = models.ForeignKey(
        "Region",
        null=True,
        related_name="stores",
        on_delete=models.SET_NULL,
    )
    city = models.ForeignKey(
        "City",
        null=True,
        related_name="stores",
        on_delete=models.SET_NULL,
    )
    postal_code = models.IntegerField(null=True, blank=True)

    @property
    def region_code(self):
        return self.region_id

    @property
    def city_name(self):
        if self.city:
            return self.city.name
        return ""

    @property
    def region_name(self):
        if self.region:
            return self.region.name
        return ""


class Item(models.Model):
    gtin = models.CharField(max_length=32, unique=True, db_index=True)
    member = models.ForeignKey("Member", related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    product_short_name = models.CharField(max_length=250)
    tnved = models.CharField(max_length=32, db_index=True)
    tnved10 = models.CharField(max_length=32, db_index=True)
    brand = models.CharField(max_length=250)
    country = models.CharField(max_length=100, blank=True)
    volume = models.FloatField()

    def __str__(self):
        return self.product_name


class Member(models.Model):
    inn = models.CharField(max_length=32, unique=True, db_index=True)
    region = models.ForeignKey(
        "Region",
        null=True,
        related_name="members",
        on_delete=models.SET_NULL,
    )


class StoreExport(models.Model):
    store = models.ForeignKey("Store", related_name="exports", on_delete=models.CASCADE)
    file = models.FileField(upload_to="exports/")

    def __str__(self):
        return f"export file from {self.store}"


class ItemSale(models.Model):
    date = models.DateField()
    region = models.ForeignKey("Region", related_name="sales", on_delete=models.CASCADE)
    type_operation = models.CharField(max_length=50)
    cnt = models.IntegerField()


class ItemTransaction(models.Model):
    date = models.DateField()
    region = models.ForeignKey(
        "Region", related_name="transactions", on_delete=models.CASCADE
    )
    sender_region_code = models.IntegerField()
    cnt = models.IntegerField()


class StoreItem(models.Model):
    store = models.ForeignKey("Store", related_name="sales", on_delete=models.CASCADE)
    item = models.ForeignKey("Item", related_name="sales", on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField()

    class Meta:
        ordering = ["-date"]
