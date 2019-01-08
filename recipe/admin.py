from django.contrib import admin
from .models import Recipe, Comment, Ingredient, Category

admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Ingredient)