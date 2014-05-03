from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView, FormView, ListView

from .forms import LetterGradeFormSet, SemesterForm, UClassFormSet
from .models import calculate_gpa, LetterGrade, Semester, UClass

def create_semester(request):
    # If POST, validate both forms, save, and redirect to index
    if request.method == 'POST': 
        semesterForm = SemesterForm(request.POST)
        classesFormSet = UClassFormSet(request.POST)
        
        if semesterForm.is_valid() and classesFormSet.is_valid():
            semesterInstance = semesterForm.save()
            
            for form in classesFormSet:
                form.instance.semester_id = semesterInstance.id

            classesFormSet.save()
            
            return HttpResponseRedirect(reverse_lazy('semester_index'))
    
    # If GET, prepare empty forms.
    else:
        semesterForm = SemesterForm()
        classesFormSet = UClassFormSet(queryset=UClass.objects.none())
        
    # Note if either form invalid in a POST, control jumps here and page
    # reloaded with forms containing error messages, etc.
    return render(request, 'core/semester_create.html', {
        'semester_form' : semesterForm,
        'classes_formset' : classesFormSet,
        'is_update' : False
    })

def update_semester(request, pk):
    semester_id = pk
    
    # If POST, validate both forms, save, and redirect to index
    if request.method == 'POST': 
        semesterForm = SemesterForm(request.POST)
        classesFormSet = UClassFormSet(request.POST)
        classesFormSet.can_delete = True 
        
        if semesterForm.is_valid() and classesFormSet.is_valid():
            semesterForm.instance.id = semester_id
            semesterForm.save()
            
            for form in classesFormSet:
                form.instance.semester_id = semester_id

            classesFormSet.save()
            
            return HttpResponseRedirect(reverse_lazy('semester_index'))
    
    # If GET, grab semester and its classes via pk, and instantiate forms
    # with that data.
    else:
        semesterForm = SemesterForm(
            instance=Semester.objects.get(id=semester_id)
        )
        classesFormSet = UClassFormSet(
            queryset=UClass.objects.filter(semester=semester_id),
        )
        
        # Class deletion allowed here; Semester deletion handled in 
        # SemesterDeleteView
        classesFormSet.can_delete = True 

    # Note if either form invalid in a POST, control jumps here and page
    # reloaded with forms containing error messages, etc.
    return render(request, 'core/semester_create.html', {
        'semester_form' : semesterForm,
        'classes_formset' : classesFormSet,
        'is_update' : True
    })
    
class GradeScaleUpdateView(FormView):
    model = LetterGrade
    form_class = LetterGradeFormSet
    template_name = 'core/gradescale_update.html'
    success_url = reverse_lazy('semester_index')
    
    # TODO: Once users implemented, use user key to get correct scale.
    queryset = LetterGrade.objects.filter(scale=1)

    def post(self, request, *args, **kwargs):
        formset = LetterGradeFormSet(request.POST)
        for form in formset:
            # TODO: Once users implemented, use user key to get correct
            # scale.
            form.instance.scale_id = 1
        
        if formset.is_valid():
            formset.save()
            
            return HttpResponseRedirect(reverse_lazy('semester_index'))
        
        context = self.get_context_data(form=formset)
        return render(request, self.template_name, context)

class SemestersIndex(ListView):
    queryset = Semester.objects.select_related('uclass')
    
    def get_context_data(self, **kwargs):
        kwargs['cumulative_gpa'] = calculate_gpa(UClass.objects.all())
        return super().get_context_data(**kwargs)

class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'core/semester_delete.html'
    success_url = reverse_lazy('semester_index')
