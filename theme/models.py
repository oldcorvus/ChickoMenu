from django.db import models
from utils.models import TimeStampedUUIDModel

class Theme(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to='theme_preview',blank=True, null=True)
    background_image = models.ImageField(upload_to='theme_image', blank=True, null=True)
    font_family = models.CharField(max_length=255, default='Arial, sans-serif')
    menu_background_color = models.CharField(max_length=7, default='#f8f9fa')
    menu_text_color = models.CharField(max_length=7, default='#343a40')

    def __str__(self):
        return self.name