from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView, FormView, ListView

from .forms import SemesterForm, UClassFormSet
from .models import (calculate_gpa, Semester, Session,
    UClass)

def create_semester(request):
    # If POST, validate both forms, save, and redirect to index
    if request.method == 'POST': 
        semesterForm = SemesterForm(request.POST)
        classesFormSet = UClassFormSet(request.POST)
        
        if semesterForm.is_valid() and classesFormSet.is_valid():
            semesterInstance = semesterForm.save(commit=False)
            semesterInstance.session = Session.objects.get(
                    pk=request.session.session_key
            )
            semesterInstance.save()
            
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
    # Ensure users can only access semesters from their own session
    try:
        semester = Semester.objects.get(pk=pk, 
            session=request.session.session_key
        )
    except ObjectDoesNotExist:
        raise Http404
    
    # If POST, validate both forms, save, and redirect to index
    if request.method == 'POST': 
        semesterForm = SemesterForm(request.POST)
        classesFormSet = UClassFormSet(request.POST)
        classesFormSet.can_delete = True 
        
        if semesterForm.is_valid() and classesFormSet.is_valid():
            semesterForm.instance.id = semester.id
            semesterForm.instance.session = Session.objects.get(
                pk=request.session.session_key
            )
            semesterForm.save()
            
            for form in classesFormSet:
                form.instance.semester_id = semester.id

            classesFormSet.save()
            
            return HttpResponseRedirect(reverse_lazy('semester_index'))
    
    # If GET, grab semester and its classes via pk, and instantiate forms
    # with that data.
    else:
        semesterForm = SemesterForm(
            instance=semester
        )
        classesFormSet = UClassFormSet(
            queryset=UClass.objects.filter(semester=semester.id),
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

class SemestersIndex(ListView):
    def get(self, request, *args, **kwargs):
        session_key = ''
        
        if not request.session.session_key:
            request.session.modified = True
        else:
            session_key = request.session.session_key
        
        self.object_list = self.get_queryset(session_key=session_key)
        context = self.get_context_data(session_key=session_key)
        
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        kwargs['cumulative_gpa'] = calculate_gpa(UClass.objects.filter(semester__session=kwargs['session_key']))
        return super().get_context_data(**kwargs)
        
    def get_queryset(self, **kwargs):
        session_key = kwargs.get('session_key')
        
        return Semester.objects.filter(session=session_key).select_related('uclass')

class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'core/semester_delete.html'
    success_url = reverse_lazy('semester_index')
