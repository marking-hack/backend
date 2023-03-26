from django.urls import path, include

app_name = "api"
urlpatterns = [path("", include("marking_hack.market.api.urls"))]
