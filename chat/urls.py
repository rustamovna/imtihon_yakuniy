from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),  
    path('start/<int:ad_id>/', views.start_thread, name='start_thread'),
]
