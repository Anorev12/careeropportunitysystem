from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Applicant, Administrator


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ('username', 'fullname', 'email', 'phone_number', 'role', 'status', 'date_joined')
    list_filter   = ('role', 'status', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering      = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Career Opportunity System', {
            'fields': ('phone_number', 'role', 'status')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Career Opportunity System', {
            'fields': ('phone_number', 'role', 'status')
        }),
    )


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display  = ('user', 'address', 'date_assigned', 'availability_status')
    list_filter   = ('availability_status',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'address')
    raw_id_fields = ('user',)


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display  = ('user', 'employee_number', 'department', 'date_assigned', 'permissions_level')
    list_filter   = ('permissions_level', 'department')
    search_fields = ('user__username', 'employee_number', 'department')
    raw_id_fields = ('user',)