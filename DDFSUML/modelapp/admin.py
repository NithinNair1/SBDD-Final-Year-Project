from django.contrib import admin
from .models import Symp,DiseaseDesc,About,Profile,queryToDoc
# Register your models here.
admin.site.register(Symp)
admin.site.register(DiseaseDesc)
admin.site.register(About)
admin.site.register(queryToDoc)
admin.site.register(Profile)
