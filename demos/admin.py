from django.contrib import admin
from .models import Bank, DemoModel, Sample, FileUpload
# Register your models here.

admin.site.register(Bank)
admin.site.register(Sample)
admin.site.register(DemoModel)
admin.site.register(FileUpload)
