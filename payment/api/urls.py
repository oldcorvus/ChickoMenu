from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView

app_name = "payment"

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order_list_create'),
    path('orders/<str:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),


]