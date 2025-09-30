from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self): return self.name

class Ad(models.Model):
    STATUS_CHOICES = [('draft','Draft'), ('active','Active'), ('blocked','Blocked')]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self): 
        return self.title

class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ad_images/', blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self): return f"Image for {self.ad.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad')

class Complaint(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='complaints')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shikoyat: {self.ad.title} - {self.user.username}"
