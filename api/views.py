from rest_framework.generics import get_object_or_404
from recipe.models import Follow, Ingredient, ShopList, Recipe, Favorite, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class PurchaseView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        recipe_id = request.data.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShopList.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({"success": True})

    def delete(self, request, id):
        shop = ShopList.objects.filter(user=request.user, recipe=id).delete()
        return Response({"success": True})

class FavoritesView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        recipe_id = request.data.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({"success": True})
    
    def delete(self, request, id):
        Favorite.objects.filter(user=request.user, recipe=id).delete()
        return Response({"success": True})

class SubscriptionsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        author_id = request.data.get("id")
        author = User.objects.get(id=author_id)
        Follow.objects.get_or_create(user=request.user, author=author)
        return Response({"success": True})
    def delete(self, request, id):
        User.objects.get(id=id)
        Follow.objects.filter(user=request.user, author=id).delete()
        return Response({"success": True})

class IngredientsView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = request.GET.get("query")
        recipes = Ingredient.objects.filter(title__startswith=query).values('title','unit')
        return Response(recipes)
