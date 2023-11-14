from django.db import models
from django.contrib.auth.models import User
import hashlib

# Create your models here.

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.URLField()

    # field to store the SHA-256 hash of the file
    file_hash = models.CharField(max_length=64, default='')

    # new field to store shared users on Posgre
    shared_with = models.ManyToManyField(User, related_name = 'shared_files', blank = True)

    # for debugging
    def __str__(self):
        return f"{self.user.username}'s file"
    

