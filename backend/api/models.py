from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, blank=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated']
