from django.db import models

# Create your models here.

class Semester(models.Model):
    pass

class UClass(models.Model):
    semester = models.ForeignKey(Semester)
    name = models.CharField(max_length=30)
    credits = models.PositiveSmallIntegerField
    grade = models.DecimalField(max_digits=4, decimal_places=3)