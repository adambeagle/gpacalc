from django.forms import ModelForm, ValidationError
from django.forms.models import (BaseModelFormSet, modelform_factory, 
    modelformset_factory)

from .models import LetterGrade, Semester, UClass

class LetterGradeForm(ModelForm):
    error_css_class = 'form-field-error'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descriptor'].widget.attrs.update(
            {'class' : 'small-text-input'}
        )
        
        self.fields['descriptor'].label = 'Grade'
        
    class Meta:
        model = LetterGrade
        fields = ['descriptor', 'value']

class UClassForm(ModelForm):
    error_css_class = 'form-field-error'
    required_css_class = 'form-field-required'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].widget.attrs.update(
            # Note Decimal attributes in model give an effective
            # 'max' of 9.999 for this field.
            {'min' : '0.0',}
        )
        
    class Meta:
        model = UClass
        fields = ['name', 'credits', 'grade']

class BaseLetterGradeFormSet(BaseModelFormSet):
    def clean(self):
        """
        Ensure 'descriptor' fields in an individual form are unique. 
        This enforces the unique_together attribute of the LetterGrade model
        without the need for the 'scale' field to be included in the forms.
        
        If duplicate descriptors found, errors are attached to both offending
        fields, and ValidationError is raised (creating an error in 
        self.non_form_errors).
        """
        descriptors = []
        
        if any(self.errors):
            return
        
        for i, form in enumerate(self.forms):
            # Skip entirely blank forms
            if not form.cleaned_data:
                continue
                
            d = form.cleaned_data['descriptor']
            if d in descriptors:
                dupI = descriptors.index(d)
                msg = 'Duplicate grades found. Grades must be distinct.'
                self.errors[i]['descriptor'] = [msg]
                self.errors[dupI]['descriptor'] = [msg]
                
                raise ValidationError('Grades must be distinct. Duplicate found.')
            
            descriptors.append(d)


LetterGradeFormSet = modelformset_factory(
    LetterGrade,
    form=LetterGradeForm,
    formset=BaseLetterGradeFormSet,
    extra=2
)

UClassFormSet = modelformset_factory(
    UClass, 
    form=UClassForm,
    extra=5,
)

SemesterForm = modelform_factory(Semester, fields=['description'])