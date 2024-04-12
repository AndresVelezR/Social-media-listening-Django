from django.db import models
from django.contrib.auth.models import User
import numpy as np


def get_default_array():
  default_arr = np.random.rand(1536)  # Adjust this to your desired default array
  return default_arr.tobytes()

class Comment(models.Model):
   
    user_tag = models.CharField(max_length=100)
    tweet = models.TextField(max_length=1000)
    time = models.CharField(max_length=100)
    reply = models.IntegerField(blank=True, null=True)
    retweet = models.IntegerField(blank=True, null=True)
    like = models.IntegerField(blank=True, null=True)
    visualizations = models.IntegerField(blank=True, null=True)
    analysis = models.TextField(max_length=2000)
    clasification = models.CharField(max_length=11)
    emb = models.BinaryField(default=get_default_array())
    

    def __str__(self):
        return self.title
