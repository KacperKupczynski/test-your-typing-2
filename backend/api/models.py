from django.db import models

class Text(models.Model):
    content = models.TextField(unique=True)
    def __str__(self):
        return self.content