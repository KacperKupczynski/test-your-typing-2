from django.db import models

class Text(models.Model):
    content = models.TextField(unique=True)
    def __str__(self):
        return self.content

class WpmResult(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    wpm = models.IntegerField()
    time = models.FloatField()
    user = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WPM: {self.wpm}, Text: {self.text.content[:20]}..."
    # additional definitions for the WpmResult model can be added here
    class Meta:
        ordering = ['-created_at']
        verbose_name = "WPM Result"
        verbose_name_plural = "WPM Results"