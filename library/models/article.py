from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    title = models.CharField(max_length=200)
    preview_text = models.TextField()
    preview_img = models.ImageField(upload_to='images/articles/', blank=True, null=True, max_length=500)
    data = models.BinaryField(null=True, blank=True)