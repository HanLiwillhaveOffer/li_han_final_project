from django import forms


from .models import Recipe, Comment, Category, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title','category','ingredient','step')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('rate','text')

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_name',)

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('ingredient_name',)

