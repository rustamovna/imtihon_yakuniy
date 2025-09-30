from django.urls import path
from .views import (
    AdListView, AdDetailView, AdCreateView, AdEditView,
    ToggleFavoriteView, SearchView, AdsByCategoryView,
    FavoritesView, AddComplaintView
)

app_name = 'ads'

urlpatterns = [
    path('', AdListView.as_view(), name='list'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='detail'),
    path('add/', AdCreateView.as_view(), name='add'),
    path('ad/<int:pk>/edit/', AdEditView.as_view(), name='edit'),
    path('favorite/<int:pk>/', ToggleFavoriteView.as_view(), name='toggle_fav'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<int:category_id>/', AdsByCategoryView.as_view(), name='by_category'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('ad/<int:ad_id>/complaint/', AddComplaintView.as_view(), name='add_complaint'),
]
