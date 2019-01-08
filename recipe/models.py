from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.urls import reverse

RATE_CHOICES = (
    (1,'extremely low'),
    (2,'low'),
    (3,'medium'),
    (4,'high'),
    (5,'extremely high'),
)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('category_detail',
                       kwargs = {'pk':self.pk})

    def get_update_url(self):
        return reverse('category_update',
                       kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('category_delete',
                       kwargs={'pk':self.pk})

    class Meta:
        ordering = ['category_name']


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length = 20,unique=True)

    def __str__(self):
        return self.ingredient_name

    def get_absolute_url(self):
        return reverse('ingredient_detail',
                       kwargs = {'pk':self.pk})

    def get_update_url(self):
        return reverse('ingredient_update',
                       kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('ingredient_delete',
                       kwargs={'pk':self.pk})

    class Meta:
        ordering = ['ingredient_name']


class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    step = models.TextField()
    ingredient = models.ForeignKey(Ingredient,on_delete=models.PROTECT,related_name='recipes')
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='recipes')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def average_rate_score(self):
        if self.comments.aggregate(Avg('rate'))['rate__avg']==None:
            return 0
        else:
            return round(self.comments.aggregate(Avg('rate'))['rate__avg'],1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail',
                       kwargs = {'pk':self.pk})

    def get_update_url(self):
        return reverse('recipe_update',
                       kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('recipe_delete',
                       kwargs={'pk':self.pk})

    class Meta:
        ordering = ['title']

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey('recipe.Recipe', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    def get_update_url(self):
        return reverse('comment_update',kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('comment_delete',
                       kwargs={'pk':self.pk})



