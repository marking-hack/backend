from django.urls import path

from . import views

app_name = "market"

urlpatterns = [
    path("", views.ListStore.as_view()),
    path("predict", views.PredictItemsView.as_view()),
    path("<str:id_sp>", views.ListStoreItems.as_view()),
    path("regions/", views.RegionListView.as_view()),
    path("regions/<int:code>/sales", views.RegionSalesListView.as_view()),
    path(
        "regions/<int:code>/trsansactions", views.RegionTransactionsListView.as_view()
    ),
]
