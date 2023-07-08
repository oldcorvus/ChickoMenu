from django.urls import path
from .views import ThemeListCreateAPIView, ThemeRetrieveUpdateDestroyAPIView

app_name = "theme"

urlpatterns = [
    path('themes/', ThemeListCreateAPIView.as_view(), name='theme-list'),
    path('themes/<str:pk>/', ThemeRetrieveUpdateDestroyAPIView.as_view(), name='theme-detail'),
]