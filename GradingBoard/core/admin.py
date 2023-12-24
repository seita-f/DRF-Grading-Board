"""
Django Admin Customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _  # auto translation
from django import forms

from . import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin page for users """
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), ({'fields': ('last_login',)})),
    )
    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


# class PostAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.Post
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Add filtering to school, faculty, class_name, and professor based on each other
#         if 'school' in self.fields:
#             self.fields['faculty'].queryset = models.Faculty.objects.none()
#             self.fields['class_name'].queryset = models.Class.objects.none()
#             self.fields['professor'].queryset = models.Professor.objects.none()
#
#             if 'school' in self.data:
#                 try:
#                     school_id = int(self.data.get('school'))
#                     self.fields['faculty'].queryset = models.Faculty.objects.filter(school_id=school_id)
#                 except (ValueError, TypeError):
#                     pass
#
#             if 'faculty' in self.data:
#                 try:
#                     faculty_id = int(self.data.get('faculty'))
#                     self.fields['class_name'].queryset = models.Class.objects.filter(faculty_id=faculty_id)
#                     self.fields['professor'].queryset = models.Professor.objects.filter(faculty_id=faculty_id)
#                 except (ValueError, TypeError):
#                     pass
#
#             elif self.instance.pk:
#                 self.fields['faculty'].queryset = self.instance.school.faculty_set
#                 self.fields['class_name'].queryset = self.instance.faculty.class_set
#                 self.fields['professor'].queryset = self.instance.faculty.professor_set
#
#
# class PostAdmin(admin.ModelAdmin):
#     form = PostAdminForm


admin.site.register(models.User, UserAdmin)
admin.site.register(models.School)
admin.site.register(models.Faculty)
admin.site.register(models.Class)
admin.site.register(models.Professor)
admin.site.register(models.Post)
admin.site.register(models.Comment)
