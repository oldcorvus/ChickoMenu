from django.db import models
from utils.models import TimeStampedUUIDModel

class Theme(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='theme_preview',blank=True, null=True)
    font_family = models.CharField(max_length=255, default='Vazir')
    menu_background_color = models.CharField(max_length=7, default='#fff')
    menu_text_color = models.CharField(max_length=7, default='#000')
    logo_image = models.ImageField(upload_to='theme_image', blank=True, null=True)
    header_color = models.CharField(max_length=7, default='#2196f3')
    header_image = models.ImageField(upload_to='theme_image', blank=True, null=True)

    def __str__(self):
        return self.name