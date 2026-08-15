from django.db import models

# Create your models here.
class User():
    class Role(models.TextChoices):
        PATIENT = 'PATIENT', 'Patient'
        CAREGIVER = 'CAREGIVER', 'Caregiver'
        CLINICIAN = 'CLINICIAN', 'Clinician'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Patient Profile for {self.user.get_full_name() or self.user.username}"
    

class CaregiverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caregiver_profile')
    patients = models.ManyToManyField(PatientProfile, related_name='caregivers')

class ClinicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clinician_profile')
    patients = models.ManyToManyField(PatientProfile, related_name='clinicians')


class Medication(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50) # e.g, "500mg", "1 tablet", etc.
    frequency = models.CharField(max_length=50) # e.g, "Once a day", "Twice a day", etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.dosage}) for {self.patient.user.get_full_name() or self.patient.user.username}"
    

class AdherenceLog(models.Model):
    class Status(models.TextChoices):
        TAKEN = 'TAKEN', 'Taken'
        MISSED = 'MISSED', 'Missed'
        SKIPPED = 'SKIPPED', 'Skipped'

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='adherence_logs')
    scheduled_time = models.DateTimeField()
    logged_at = models.DateTimeField(default=models.timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-logged_at']