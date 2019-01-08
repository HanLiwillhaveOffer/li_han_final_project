from django.urls import path
from . import views
from recipe.views import (
    RecipeList, RecipeDetail, RecipeCreate, RecipeUpdate, RecipeDelete, PublishedRecipeList,
    CommentDelete, CategoryList, CategoryDetail, CategoryUpdate, CategoryCreate, CategoryDelete, IngredientList,
    IngredientDetail, IngredientUpdate, IngredientCreate, IngredientDelete, CommentUpdate)
urlpatterns = [
    path('recipe/',
         RecipeList.as_view(), name='recipe_list'),

    path('publishedrecipe/',
         PublishedRecipeList.as_view(),name = 'published_recipe_list'),

    path('recipe/<int:pk>/',
         RecipeDetail.as_view(), name='recipe_detail'),

    path('recipe/<int:pk>/update/',
         RecipeUpdate.as_view(), name='recipe_update'),

    path('recipe/new',
         RecipeCreate.as_view(), name='recipe_create'),

    path('recipe/<int:pk>/publish/', views.recipe_publish, name='recipe_publish'),

    path('recipe/<int:pk>/delete/',
         RecipeDelete.as_view(), name='recipe_delete'),

    path('recipe/<int:pk>/comment/',
         views.add_comment_to_recipe, name='add_comment_to_recipe'),

    path('comment/<int:pk>/update/',
         CommentUpdate.as_view(), name='comment_update'),

    path('comment/<int:pk>/delete/',
        CommentDelete.as_view(), name='comment_delete'),

    path('category/',
         CategoryList.as_view(), name='category_list'),

    path('category/<int:pk>/',
         CategoryDetail.as_view(), name='category_detail'),

    path('category/<int:pk>/update/',
         CategoryUpdate.as_view(), name='category_update'),

    path('category/new',
         CategoryCreate.as_view(), name='category_create'),

    path('category/<int:pk>/delete/',
         CategoryDelete.as_view(), name='category_delete'),

    path('ingredient/',
         IngredientList.as_view(), name='ingredient_list'),

    path('ingredient/<int:pk>/',
         IngredientDetail.as_view(), name='ingredient_detail'),

    path('ingredient/<int:pk>/update/',
         IngredientUpdate.as_view(), name='ingredient_update'),

    path('ingredient/new',
         IngredientCreate.as_view(), name='ingredient_create'),

    path('ingredient/<int:pk>/delete/',
         IngredientDelete.as_view(), name='ingredient_delete'),
]
