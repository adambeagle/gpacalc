from django.contrib import admin

from .models import Semester, UClass

class UClassInline(admin.TabularInline):
    model = UClass
    extra = 1

class SemesterAdmin(admin.ModelAdmin):
    model = Semester
    inlines = [UClassInline]

admin.site.register(Semester, SemesterAdmin)