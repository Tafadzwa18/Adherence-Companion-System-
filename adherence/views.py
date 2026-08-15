from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medication, AdherenceLog, PatientProfile
from .permissions import PatientDataAccessMixin

# --- Medication CRUD ---

class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'adherence/medication_list.html'
    context_object_name = 'medications'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PATIENT':
            return Medication.objects.filter(patient=user.patient_profile)
        elif user.role in ['CAREGIVER', 'CLINICIAN']:
            # List all medications for patients assigned to this caregiver/clinician
            return Medication.objects.filter(
                patient__in=getattr(user, f"{user.role.lower()}_profile").patients.all()
            )
        return Medication.objects.none()

class MedicationCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    fields = ['name', 'dosage', 'frequency']
    template_name = 'adherence/medication_form.html'
    success_url = reverse_lazy('medication-list')

    def form_valid(self, form):
        # Automatically tie medication to the logged-in patient
        form.instance.patient = self.request.user.patient_profile
        return super().form_valid(form)

# --- Adherence Logging CRUD ---

class AdherenceLogCreateView(LoginRequiredMixin, CreateView):
    model = AdherenceLog
    fields = ['medication', 'scheduled_time', 'status', 'notes']
    template_name = 'adherence/log_form.html'
    success_url = reverse_lazy('medication-list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Restrict medication choices to current user's profile
        if self.request.user.role == 'PATIENT':
            form.fields['medication'].queryset = Medication.objects.filter(
                patient=self.request.user.patient_profile
            )
        return form