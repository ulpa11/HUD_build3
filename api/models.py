from django.db import models
import uuid
from django.contrib.auth.models import User
from .validators import validate_photo_file_extension,validate_audio_file_extension
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(('admin', 'admin'), ('developer', 'developer'), ('operator', 'operator')),default='operator')
    def __str__(self):
        return self.user.username

#Common Machine Setting that saves audio
class CommonMachineSetting(models.Model):
    common_machine_setting_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audio1 = models.FileField(upload_to='common_audio_settings', blank=True,validators=[validate_audio_file_extension])
    audio2 = models.FileField(upload_to='common_audio_settings', blank=True,validators=[validate_audio_file_extension])
    audio3 = models.FileField(upload_to='common_audio_settings', blank=True,validators=[validate_audio_file_extension])
    audio4 = models.FileField(upload_to='common_audio_settings', blank=True,validators=[validate_audio_file_extension])
    audio5 = models.FileField(upload_to='common_audio_settings', blank=True,validators=[validate_audio_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Machine Setting that saves audio
class UniqueMachineSetting(models.Model):
    unique_machine_setting_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audio6 = models.FileField(upload_to='machine_audio_settings',blank=True,validators=[validate_audio_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Machine Model
class Machine(models.Model):
    machine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    machine_name = models.CharField(max_length=100, blank=False,unique=True)
    machine_country = models.CharField(max_length=50, blank=True)
    machine_state = models.CharField(max_length=50, blank=True)
    machine_city = models.CharField(max_length=50, blank=True)
    machine_status=models.CharField(max_length=3, blank=True,default="off")
    common_machine_setting = models.ForeignKey(CommonMachineSetting, on_delete=models.CASCADE,blank=True,null=True)
    machine_setting=models.ForeignKey(UniqueMachineSetting,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.machine_name

# Medicine Model
class Medicine(models.Model):
    medicine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MedicineTablet(models.Model):
    medicine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=200, blank=True, default="tablet")
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MedicineOintment(models.Model):
    medicine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=200, blank=True, default="ointment")
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PatientHistoryPhotos(models.Model):
    PatientHistoryPhotos_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to='patient_history_photos', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Patient History Model
class PatientHistory(models.Model):
    patient_history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    duration = models.CharField(max_length=100, blank=True)
    thyroid = models.CharField(max_length=100, blank=True)
    auto_imm_dis = models.CharField(max_length=100, blank=True)
    jaundice = models.CharField(max_length=100, blank=True)
    fh_auto_imm_dis = models.CharField(max_length=100, blank=True)
    ophthalmological_problems = models.CharField(max_length=100, blank=True)
    hospitalization = models.CharField(max_length=100, blank=True)
    psychiatric_history = models.CharField(max_length=100, blank=True)
    keloidol_tendency = models.CharField(max_length=100, blank=True)
    epilepsy = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=100, blank=True)
    steroid_history = models.CharField(max_length=100, blank=True)
    photo_of_date = models.ManyToManyField(PatientHistoryPhotos, blank=True)
    antibodies_to_thyroid = models.CharField(max_length=100, blank=True)
    h_o_epilepsy = models.CharField(max_length=100, blank=True)
    activity = models.CharField(max_length=100, blank=True)
    fh_b_vitiligo = models.CharField(max_length=100, blank=True)
    h_o_thyroid = models.CharField(max_length=100, blank=True)
    hb_value=models.CharField(max_length=100, blank=True)
    rating=models.CharField(max_length=100, blank=True)
    # add one to many relationship with medicine
    medicine = models.ManyToManyField(Medicine, blank=True)
    medicine_tablet = models.ManyToManyField(MedicineTablet, blank=True)
    medicine_ointment = models.ManyToManyField(MedicineOintment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Patient(models.Model):
    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200, blank=False)
    patient_type = models.CharField(max_length=200, blank=True)
    date_of_birth = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200, blank=False, unique=True)
    skin_type = models.CharField(max_length=200, blank=True)
    system_code=models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='patient_photo', blank=True)
    # connect machine to it
    machine_id=models.ForeignKey(Machine,on_delete=models.CASCADE,blank=True,null=True)
    patient_history_id = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class PackageComment(models.Model):
    package_comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Package(models.Model):
    package_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package_name = models.CharField(max_length=200, blank=False, unique=False)
    package_status = models.CharField(max_length=200, blank=True)
    package_comment = models.ManyToManyField(PackageComment, blank=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)#removed blank=true
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.package_name

class DoseComment(models.Model):
    dose_comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Dose(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    dose_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    j_cm2 = models.FloatField(blank=False)
    # select from tube a or b
    choices = (('Tube A', 'Tube A'), ('Tube B', 'Tube B'))
    tube = models.CharField(max_length=200, blank=False, choices=choices)
    # in date recored the current date and time
    dose_comments=models.ManyToManyField(DoseComment,blank=True)
    status = (
    ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Paused', 'Paused'), ('Completed', 'Completed'))
    status = models.CharField(max_length=200, choices=status, default='Not Started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DoctorViewStorage(models.Model):
    doctor_view_storage_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    index=models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    