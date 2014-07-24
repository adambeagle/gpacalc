from django.contrib import admin

from .models import LetterGrade, Semester, UClass

class UClassInline(admin.TabularInline):
    model = UClass
    extra = 1

class SemesterAdmin(admin.ModelAdmin):
    model = Semester
    fields = ['description']
    inlines = [UClassInline]

admin.site.register(LetterGrade)
admin.site.register(Semester, SemesterAdmin)