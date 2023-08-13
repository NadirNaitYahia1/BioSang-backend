from django.contrib import admin
import api.models as models
# Register your models here.
admin.site.register(models.Patient)
admin.site.register(models.Admin)
admin.site.register(models.Cliche)
admin.site.register(models.Analyse)

