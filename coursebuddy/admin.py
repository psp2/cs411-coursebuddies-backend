from django.contrib import admin

# Register your models here.
from . import *

admin.site.register(models.ProfessorRatingsFromUser)
admin.site.register(models.ProfessorRatingsFromWebsites)
admin.site.register(models.Studygroup)
admin.site.register(models.Login)
admin.site.register(models.Sp19)