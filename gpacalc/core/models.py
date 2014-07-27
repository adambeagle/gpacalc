from decimal import Decimal

from django.contrib.sessions.models import Session
from django.db import models

GRADES = {
    'A+' : 4.3,
    'A' : 4.0,
    'A-' : 3.7,
    'B+' : 3.5,
    'B' : 3.0,
    'B-' : 2.7,
    'C+' : 2.5,
    'C' : 2.0,
    'C-' : 1.7,
    'D+' : 1.5,
    'D' : 1.0,
    'S' : 0.0,
    'H' : 0.0
}

for g in GRADES:
    GRADES[g] = Decimal(GRADES[g])

SORTED_GRADES = reversed(sorted(GRADES.keys(), key=lambda x: GRADES[x]))

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
        grade = GRADES[c.grade]
        
        # 'S' and 'H' courses do not count toward GPA,
        # so ignore courses with grade 0.0
        if grade:
            totalCredits += c.credits
            totalGrade += c.credits * grade
        
    return totalGrade / totalCredits

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
    GRADE_CHOICES = [(g, g) for g in SORTED_GRADES]
    
    semester = models.ForeignKey(Semester)
    name = models.CharField(max_length=30, blank=True)
    credits = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
        
    def __str__(self):
        return self.name