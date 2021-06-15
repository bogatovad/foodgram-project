from django.urls import path
from .views import (PurchaseView, FavoritesView,
                    SubscriptionsView, IngredientsView)

urlpatterns = [
    path("v1/purchases/", PurchaseView.as_view()),
    path("v1/purchases/<int:id>/", PurchaseView.as_view()),
    path("v1/favorites/", FavoritesView.as_view()),
    path("v1/favorites/<int:id>/", FavoritesView.as_view()),
    path("v1/subscriptions/", SubscriptionsView.as_view()),
    path("v1/subscriptions/<int:id>/", SubscriptionsView.as_view()),
    path("v1/ingredients", IngredientsView.as_view()),
]
