from django.urls import path
from django.urls.conf import include

from .views import (FavoritesView, IngredientsView, PurchaseView,
                    SubscriptionsView)

api_urls = [
    path("purchases/",
         PurchaseView.as_view(),
         name="purchases"),
    path("purchases/<int:id>/",
         PurchaseView.as_view(),
         name="purchases_detail"),

    path("favorites/",
         FavoritesView.as_view(),
         name="favorites"),
    path("favorites/<int:id>/",
         FavoritesView.as_view(),
         name="favorite_detail"),

    path("subscriptions/",
         SubscriptionsView.as_view(),
         name="subscriptions"),
    path("subscriptions/<int:id>/",
         SubscriptionsView.as_view(),
         name="subscriptions_detail"),

    path("ingredients",
         IngredientsView.as_view(),
         name="ingredients"),

]

urlpatterns = [
    path("v1/", include(api_urls)),
]
