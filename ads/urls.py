from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.ad_list, name='list'),
    path('ad/<int:pk>/', views.ad_detail, name='detail'),
    path('add/', views.ad_create, name='add'),
    path('ad/<int:pk>/edit/', views.ad_edit, name='edit'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_fav'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.ads_by_category, name='by_category'),  
    path('favorites/', views.favorites, name='favorites'),
    
    path('ad/<int:ad_id>/complaint/', views.add_complaint, name='add_complaint'),  

]
