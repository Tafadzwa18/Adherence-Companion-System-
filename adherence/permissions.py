from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

class PatientDataAccessMixin(LoginRequiredMixin):
    """
    Ensures that only the owner patient or their assigned caregiver/clinician can access the patient's data.
    """
    def get_patient_profile(self, patient_id):
        user = self.request.user
        if user.role == user.Role.PATIENT:
            return user.patient_profile
        elif user.role == user.Role.CAREGIVER:
            return user.caregiver_profile.patients.get(pk=patient_id)
        elif user.role == user.Role.CLINICIAN:
            return user.clinician_profile.patients.get(pk=patient_id)
        raise PermissionDenied("You do not have permission to access this patient's data.")