from django.forms import ModelForm
from django.forms.models import modelform_factory, modelformset_factory

from .models import Semester, UClass

class UClassForm(ModelForm):
    model = UClass
    fields=['name', 'credits', 'grade']
    error_css_class = 'form-field-error'
    required_css_class = 'form-field-required'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].widget.attrs.update(
            # Note Decimal attributes in model give an effective
            # 'max' of 9.999 for this field.
            {'min' : '0.0',}
        )

UClassFormset = modelformset_factory(
    UClass, 
    fields=['name', 'credits', 'grade'],
    form=UClassForm,
    extra=5,
)

SemesterForm = modelform_factory(Semester, fields=['description'])