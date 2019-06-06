from django.contrib import admin

# Register your models here.
from crmEduction import models

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','qq','name','source','consultant','content','status','date')
    list_filter = ('source','consultant','date')
    search_fields = ('qq','name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)
    list_per_page = 5
    pass

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name')
    pass

admin.site.register(models.Customers,CustomerAdmin)
admin.site.register(models.CustomersFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Courses)
admin.site.register(models.ClassTable)
admin.site.register(models.CoursesRecord)
admin.site.register(models.Branch)
admin.site.register(models.Roles)
admin.site.register(models.Payment)
admin.site.register(models.StudyRecord)
admin.site.register(models.Tag)
admin.site.register(models.UserProfiles,UserProfileAdmin)
admin.site.register(models.Menu)
