from decimal import Decimal

from django.db import models

def calculate_gpa(classes):
    if not classes:
        return 0.0
    
    totalCredits = Decimal(0.0)
    totalGrade = Decimal(0.0)
    
    for c in classes:
        totalCredits += c.credits
        totalGrade += c.credits * c.grade
        
    return totalGrade / totalCredits

class Semester(models.Model):
    description = models.CharField(max_length=25, blank=True)
    
    def __str__(self):
        if self.description:
            return self.description
        else:
            return 'Semester {0}'.format(self.id)
            
    @property
    def gpa(self):
        return calculate_gpa(self.uclass_set.all())
    
class UClass(models.Model):
    semester = models.ForeignKey(Semester)
    name = models.CharField(max_length=30)
    credits = models.PositiveSmallIntegerField()
    grade = models.DecimalField(max_digits=4, decimal_places=3)
    
    def __str__(self):
        return self.name