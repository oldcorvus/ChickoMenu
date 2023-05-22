from rest_framework import generics
from theme.models import Theme
from .serializers import ThemeSerializer
from rest_framework.permissions import IsAuthenticated


class ThemeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Theme.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ThemeSerializer

class ThemeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theme.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ThemeSerializer