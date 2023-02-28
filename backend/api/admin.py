from django.contrib import admin

from api import models


admin.site.register(models.Note)
admin.site.register(models.Category)
