from django.contrib import admin
from .models import GlucoseLevel

class GlucoseLevelAdmin(admin.ModelAdmin):
    pass

admin.site.register(GlucoseLevel, GlucoseLevelAdmin)

# Register your models here.
