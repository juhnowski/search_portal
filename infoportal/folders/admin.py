from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Folders

admin.site.register(Folders, MPTTModelAdmin)
