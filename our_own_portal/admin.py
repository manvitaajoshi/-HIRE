from django.contrib import admin
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

'''from .models import Student, Company, Job, SelectedStudent, AppliedStudent'''

'''admin.site.register(Student)
admin.site.register(Company)
admin.site.register(SelectedStudent)
admin.site.register(AppliedStudent)
admin.site.register(Job)
'''

class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)