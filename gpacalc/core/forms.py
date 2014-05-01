from django.forms.models import modelform_factory, modelformset_factory

from .models import Semester, UClass

UClassFormset = modelformset_factory(UClass, extra=5, 
            fields = ['name', 'credits', 'grade'])
            
SemesterForm = modelform_factory(Semester, fields=['description'])