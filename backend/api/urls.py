from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipes")
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
