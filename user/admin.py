from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from user.models import *

User = get_user_model()

@admin.register(User)
class LabUserAdmin(UserAdmin):
    list_display = ['username', 'name']
    list_filter = ['is_superuser']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('重要时间'), {'fields': ('last_login', 'date_joined')}),
        (_('同福打印店员工信息'), {'fields': ('name', 'memo',)}),
    )

    class Meta:
        model = User


@admin.register(UserPrintRecord)
class UserPrintRecordAdmin(admin.ModelAdmin):
    list_display = ['get_user_stu_id', 'get_user_name', 'add_time', 'file_path']

    def get_user_stu_id(self, obj):
        return obj.user.username
    get_user_stu_id.short_description = 'stu_id'

    def get_user_name(self, obj):
        return obj.user.name
    get_user_name.short_description = 'name'
