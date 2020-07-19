from django.db import models

class History(models.Model):
    user = models.CharField(max_length=255)
    date = models.DateTimeField()
    keyword = models.CharField(max_length=255)
    duration = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.user
