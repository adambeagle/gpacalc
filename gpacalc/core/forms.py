from django.forms import ModelForm, Select, ValidationError, CharField
from django.forms.widgets import Select
from django.forms.models import (BaseModelFormSet, modelform_factory, 
    modelformset_factory)

from .models import Semester, UClass

class UClassForm(ModelForm):
    error_css_class = 'form-field-error'
    required_css_class = 'form-field-required'
        
    class Meta:
        model = UClass
        fields = ['name', 'credits', 'grade']

UClassFormSet = modelformset_factory(
    UClass, 
    form=UClassForm,
    extra=5,
)

SemesterForm = modelform_factory(Semester, fields=['description'])