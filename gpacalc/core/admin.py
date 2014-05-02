from django.contrib import admin

from .models import GradeScale, LetterGrade, Semester, UClass

class LetterGradeInline(admin.TabularInline):
    model = LetterGrade
    extra = 15

class UClassInline(admin.TabularInline):
    model = UClass
    extra = 1

class GradeScaleAdmin(admin.ModelAdmin):
    model = GradeScale
    inlines = [LetterGradeInline]

class SemesterAdmin(admin.ModelAdmin):
    model = Semester
    inlines = [UClassInline]

admin.site.register(GradeScale, GradeScaleAdmin)
admin.site.register(Semester, SemesterAdmin)