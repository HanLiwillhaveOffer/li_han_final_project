from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils import timezone
from recipe.forms import RecipeForm, CommentForm, CategoryForm, IngredientForm
from recipe.utils import PageLinksMixin
from .models import (
    Recipe, Comment,
    Category, Ingredient)
from django.db.models import Avg

class RecipeList(LoginRequiredMixin,PageLinksMixin,PermissionRequiredMixin, ListView):
    paginate_by = 5
    model = Recipe
    permission_required = 'recipe.view_recipe'

    def dispatch(self, *args, **kwargs):
        return super(RecipeList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

class PublishedRecipeList(LoginRequiredMixin,PageLinksMixin, PermissionRequiredMixin,ListView):
    paginate_by = 5
    model = Recipe
    template_name = "recipe/published_recipe_list.html"
    permission_required = 'recipe.view_recipe'
    def dispatch(self, *args, **kwargs):
        return super(PublishedRecipeList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Recipe.objects.filter(published_date__isnull=False)

class RecipeDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.view_recipe'
    def get(self, request, pk):
        recipe = get_object_or_404(
            Recipe,
            pk=pk
        )
        comment_list = recipe.comments.all()
        return render(
            request,
            'recipe/recipe_detail.html',
            {'recipe':recipe,'comment_list':comment_list}
        )

class RecipeCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    form_class = RecipeForm
    model = Recipe
    permission_required = 'recipe.add_recipe'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(RecipeCreate,self).form_valid(form)

class RecipeUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    form_class =RecipeForm
    model = Recipe
    template_name = 'recipe/recipe_update.html'
    permission_required = 'recipe.change_recipe'

class RecipeDelete(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.delete_recipe'
    def get_object(self,pk):
        return get_object_or_404(
            Recipe,
            pk=pk
        )

    def get(self,request,pk):
        recipe = self.get_object(pk)
        return render(
                request,
                'recipe/recipe_confirm_delete.html',
                {'recipe':recipe}
        )

    def post(self,request,pk):
        recipe = self.get_object(pk)
        comments = recipe.comments.all()
        recipe.delete()
        comments.delete()
        return redirect('recipe_list')

def recipe_publish(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.publish()
    return redirect('recipe_detail', pk=pk)

def add_comment_to_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = CommentForm()
    return render(request, 'Recipe/add_comment_to_recipe.html', {'form': form})

class CommentUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    form_class =CommentForm
    model = Comment
    template_name = 'recipe/comment_update.html'
    permission_required = 'recipe.change_comment'

    def get_success_url(self, **kwargs):
        return self.object.recipe.get_absolute_url()

class CommentDelete(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.delete_comment'
    def get_object(self,pk):
        return get_object_or_404(
            Comment,
            pk=pk
        )

    def get(self,request,pk):
        return render(
                request,
                'recipe/comment_confirm_delete.html',
        )

    def post(self,request,pk):
        comment = self.get_object(pk)
        comment.delete()
        return redirect('recipe_detail', pk=comment.recipe.pk)


class CategoryList(LoginRequiredMixin,PageLinksMixin,PermissionRequiredMixin, ListView):
    paginate_by = 5
    model = Category
    permission_required = 'recipe.view_category'


class CategoryDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.view_category'
    def get(self, request, pk):
        category = get_object_or_404(
            Category,
            pk=pk
        )
        recipe_list = category.recipes.all()
        return render(
            request,
            'recipe/category_detail.html',
            {'category': category, 'recipe_list': recipe_list}
        )

class CategoryCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    form_class = CategoryForm
    model = Category
    permission_required = 'recipe.add_category'

class CategoryUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    form_class =CategoryForm
    model = Category
    template_name = 'recipe/category_update.html'
    permission_required = 'recipe.change_category'

class CategoryDelete(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.delete_category'

    def get_object(self,pk):
        return get_object_or_404(
            Category,
            pk=pk
        )

    def get(self,request,pk):
        category = self.get_object(pk)
        recipes = category.recipes.all()
        if recipes.count()>0:
            return render(
                request,
                'recipe/category_refuse_delete.html',
                {'category':category,
                 'recipes':recipes,}
            )
        else:
            return render(
                request,
                'recipe/category_confirm_delete.html',
                {'category':category}
            )

    def post(self,request,pk):
        category = self.get_object(pk)
        category.delete()
        return redirect('category_list')

class IngredientList(LoginRequiredMixin,PageLinksMixin, PermissionRequiredMixin,ListView):
    paginate_by = 5
    model = Ingredient
    permission_required = 'recipe.view_ingredient'


class IngredientDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.view_ingredient'
    def get(self, request, pk):
        ingredient = get_object_or_404(
            Ingredient,
            pk=pk
        )
        recipe_list = ingredient.recipes.all()
        return render(
            request,
            'recipe/ingredient_detail.html',
            {'ingredient': ingredient, 'recipe_list': recipe_list}
        )

class IngredientCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    form_class = IngredientForm
    model = Ingredient
    permission_required = 'recipe.add_ingredient'

class IngredientUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    form_class =IngredientForm
    model = Ingredient
    template_name = 'recipe/ingredient_update.html'
    permission_required = 'recipe.change_ingredient'

class IngredientDelete(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'recipe.delete_ingredient'

    def get_object(self,pk):
        return get_object_or_404(
            Ingredient,
            pk=pk
        )

    def get(self,request,pk):
        ingredient = self.get_object(pk)
        recipes = ingredient.recipes.all()
        if recipes.count()>0:
            return render(
                request,
                'recipe/ingredient_refuse_delete.html',
                {'recipes':recipes,
                 'ingredient':ingredient,}
            )
        else:
            return render(
                request,
                'recipe/ingredient_confirm_delete.html',
                {'ingredient':ingredient}
            )

    def post(self,request,pk):
        ingredient = self.get_object(pk)
        ingredient.delete()
        return redirect('ingredient_list')




