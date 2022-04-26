from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete'] #if complete, come last in order