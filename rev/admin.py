from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(orginal_Result)

admin.site.register(Revaluation)

class Regulations_with_GradesAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('Regulation','Lower_limit','Upper_limit','Grades')
admin.site.register(Regulations_with_Grades,Regulations_with_GradesAdmin)

class Subject_max_marksAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('subject_code','subject_name','branch_code','max_external_marks','max_total_marks','pass_external_marks','pass_total_marks','credits','subject_type')

admin.site.register(Subject_max_marks,Subject_max_marksAdmin)

class Revaluation_copy_Admin(admin.ModelAdmin):
    list_display = ('Hallticket','Subject_code','Subject','Internal_marks','External_marks','Second_evaluation','Third_evaluation','Total_after_revaluation','Credits','Grades','Revaluation_Status')

admin.site.register(Revaluation_copy,Revaluation_copy_Admin)