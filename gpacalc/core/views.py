from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView, ListView

from .forms import SemesterForm, UClassFormset
from .models import calculate_gpa, Semester, UClass

def create_semester(request):
    if request.method == 'POST': 
        semesterForm = SemesterForm(request.POST)
        classesFormset = UClassFormset(request.POST)
        
        if semesterForm.is_valid() and classesFormset.is_valid():
            semesterInstance = semesterForm.save()
            
            for form in classesFormset:
                form.instance.semester_id = semesterInstance.id
                
            semesterForm.save()
            classesFormset.save()
            
            return HttpResponseRedirect(reverse_lazy('semester_index'))
    else:
        semesterForm = SemesterForm()
        classesFormset = UClassFormset(queryset=UClass.objects.none())

    return render(request, 'core/semester_create.html', {
        'semester_form' : semesterForm,
        'classes_formset' : classesFormset,
        'is_update' : False
    })

def update_semester(request, pk):
    semester_id = pk
    
    if request.method == 'POST': 
        semesterForm = SemesterForm(request.POST)
        classesFormset = UClassFormset(request.POST)
        
        if semesterForm.is_valid() and classesFormset.is_valid():
            semesterForm.instance.id = semester_id
            semesterForm.save()
            
            for form in classesFormset:
                form.instance.semester_id = semester_id
                
            semesterForm.save()
            classesFormset.save()
            
            return HttpResponseRedirect(reverse_lazy('semester_index'))
    else:
        semesterForm = SemesterForm(
            instance=Semester.objects.get(id=semester_id)
        )
        classesFormset = UClassFormset(
            queryset=UClass.objects.filter(semester=semester_id),
        )
        classesFormset.can_delete = True

    return render(request, 'core/semester_create.html', {
        'semester_form' : semesterForm,
        'classes_formset' : classesFormset,
        'is_update' : True
    })

class SemestersIndex(ListView):
    queryset = Semester.objects.select_related('uclass')
    
    def get_context_data(self, **kwargs):
        kwargs['cumulative_gpa'] = calculate_gpa(UClass.objects.all())
        return super().get_context_data(**kwargs)


class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'core/semester_delete.html'
    success_url = reverse_lazy('semester_index')
