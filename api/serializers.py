from rest_framework import serializers
from .models import (CommonMachineSetting, UniqueMachineSetting, Machine,
                     Medicine, PatientHistoryPhotos, PatientHistory,Patient,
                     PackageComment, Package,
                     DoseComment, Dose,MedicineTablet,MedicineOintment,DoctorViewStorage)

class CommonMachineSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonMachineSetting
        fields = '__all__'
class UniqueMachineSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueMachineSetting
        fields = '__all__'
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
class MedicineTabletSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineTablet
        fields = '__all__'
class MedicineOintmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineOintment
        fields = '__all__'
class PatientHistoryPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistoryPhotos
        fields = '__all__'
class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = '__all__'
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
class PackageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageComment
        fields = '__all__'
class PackageSerializer(serializers.ModelSerializer):
    #package_comment=PackageCommentSerializer(many=True,read_only=True)#added
    class Meta:
        model = Package
        fields = '__all__'
class DoseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoseComment
        fields = '__all__'
class DoseSerializer(serializers.ModelSerializer):
    #dose_comment=DoseCommentSerializer(many=True,read_only=True)#added
    class Meta:
        model = Dose
        fields = '__all__'

class DoctorViewStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorViewStorage
        fields = '__all__'
#for filtering package from patient id
class PatientPackageSerializer(serializers.ModelSerializer):
    patient_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = ('package_id', 'package_name', 'package_status', 'package_comment', 'patient_uuid')

    def get_patient_uuid(self, obj):
        return str(obj.patient_id.patient_id)




