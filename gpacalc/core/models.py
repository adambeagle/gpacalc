from decimal import Decimal

from django.contrib.sessions.models import Session
from django.db import models

def calculate_gpa(classes):
    """
    Return cumulative GPA of all classes found in iterable 'classes.'
    
    Assumes each element of 'classes' has 'credits' and 'grade' attributes,
    where 'grade' is a LetterGrade object.
    """
    totalCredits = Decimal(0.0)
    totalGrade = Decimal(0.0)
    
    if not classes:
        return 0.0 # Prevents division by 0

    for c in classes:
        totalCredits += c.credits
        totalGrade += c.credits * c.grade.value
        
    return totalGrade / totalCredits

class LetterGrade(models.Model):
    """
    Represents a letter grade and its GPA value equivalent. For example, 
    a descriptor of 'A' would likely have the value 4.0.
    
    'value' is allowed to be blank/null to allow pass/fail grades that do
    not affect a cumulative GPA (common examples are 'H' and 'S').
    """
    descriptor = models.CharField(max_length=2)
    value = models.DecimalField(max_digits=4, decimal_places=3, 
        null=True, blank=True
    )
    
    def __str__(self):
        return self.descriptor
    
    class Meta:
        ordering = ['-value']

class Semester(models.Model):
    description = models.CharField(max_length=25, blank=True)
    session = models.ForeignKey(Session)
    
    class Meta:
        ordering = ['id']
    
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
    name = models.CharField(max_length=30, blank=True)
    credits = models.PositiveSmallIntegerField()
    grade = models.ForeignKey(LetterGrade)
        
    def __str__(self):
        return self.name