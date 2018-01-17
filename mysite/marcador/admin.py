from django.contrib import admin

from .models import Employee, Friend, Schedule


class DoorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'access_permission', 'password')
    list_filter = ('access_permission', 'role')
    search_fields = ['id', 'role', 'name']


admin.site.register(Employee, DoorsAdmin)
admin.site.register(Friend)
admin.site.register(Schedule)
