from django.forms import ModelForm
from django.forms.models import modelform_factory, modelformset_factory

from .models import Semester, UClass

class UClassForm(ModelForm):
    model = UClass
    fields=['name', 'credits', 'grade']
    error_css_class = 'form-field-error'
    required_css_class = 'form-field-required'

UClassFormset = modelformset_factory(
    UClass, 
    fields=['name', 'credits', 'grade'],
    form=UClassForm,
    extra=5,
)

SemesterForm = modelform_factory(Semester, fields=['description'])