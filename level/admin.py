from django.contrib import admin
from .models import Activation, LevelIncomeSettings, LevelUser, PoolUser

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from import_export import resources

# Register your models here.
class LevelResource(resources.ModelResource):
    class Meta:
        model = Activation
        fields = [f.name for f in Activation._meta.fields]

class LevelAdmin(ImportExportModelAdmin):
    resource_class = LevelResource
    list_display = [f.name for f in Activation._meta.fields]

class LevelIncomeSettingResource(resources.ModelResource):
    class Meta:
        model = LevelIncomeSettings
        fields = [f.name for f in LevelIncomeSettings._meta.fields]


class LevelIncomeSettingAdmin(ImportExportModelAdmin):
    resource_class = LevelIncomeSettingResource
    list_display = [f.name for f in LevelIncomeSettings._meta.fields]

class LevelUserAdmin(ImportExportModelAdmin):
    resource_class = LevelUser
    list_display = [f.name for f in LevelUser._meta.fields]
    search_fields = ('user_id', )


admin.site.register(Activation, LevelAdmin)
admin.site.register(LevelIncomeSettings, LevelIncomeSettingAdmin)
admin.site.register(LevelUser, LevelUserAdmin)
admin.site.register(PoolUser)