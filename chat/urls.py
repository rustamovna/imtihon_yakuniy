from django.urls import path
from .views import StartThreadView, ThreadDetailView

app_name = 'chat'

urlpatterns = [
    path('start/<int:ad_id>/', StartThreadView.as_view(), name='start_thread'),
    path('thread/<int:thread_id>/', ThreadDetailView.as_view(), name='thread_detail'),
]
