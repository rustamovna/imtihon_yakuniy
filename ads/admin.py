from django.contrib import admin
from .models import Ad, AdImage, Favorite, Category, City, Complaint

# Register your models here.

class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 0

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title','seller','price','status','created_at')
    inlines = [AdImageInline]
admin.site.register(Category)
admin.site.register(City)
admin.site.register(Favorite)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user', 'created_at')
    search_fields = ('text',)