from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, UserViewSet, TagsViewSet, IngredientViewSet

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"users", UserViewSet, basename="users")
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "recipes/<int:id>/get-link/",
        RecipeViewSet.as_view({"get": "get_link"}),
        name="get-link",
    )
]
urlpatterns += router.urls