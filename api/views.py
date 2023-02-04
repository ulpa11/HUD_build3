from django.shortcuts import render
from .models import (CommonMachineSetting, UniqueMachineSetting, Machine,
                     Medicine, PatientHistoryPhotos, PatientHistory,Patient,
                     PackageComment, Package,
                     DoseComment, Dose,MedicineTablet,MedicineOintment,
                     DoctorViewStorage)
from .serializers import (CommonMachineSettingSerializer, UniqueMachineSettingSerializer,MachineSerializer,
                        MedicineSerializer,
                        PatientHistoryPhotosSerializer, PatientHistorySerializer,PatientSerializer,
                        PackageCommentSerializer, PackageSerializer,
                        DoseCommentSerializer, DoseSerializer,MedicineTabletSerializer,MedicineOintmentSerializer,DoctorViewStorageSerializer)


from rest_framework import viewsets
#for token with roles
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from geopy.geocoders import Nominatim

def get_all_cities(request):
    geolocator = Nominatim(user_agent="geoapiExercises")
    cities = []
    for machine in Machine.objects.all():
        try:
            location = geolocator.geocode(f"{machine.machine_city}, {machine.machine_state}, {machine.machine_country}")
            cities.append({
                "machine_name": machine.machine_name,
                "machine_status": machine.machine_status,
                "city": machine.machine_city,
                "state": machine.machine_state,
                "country": machine.machine_country,
                "latitude": location.latitude,
                "longitude": location.longitude
            })
        except:
            # If the geolocator fails to get the location of the city, then the code inside this block will be executed
            print("Failed to retrieve location for", machine.machine_city, machine.machine_state, machine.machine_country)
    return JsonResponse({"cities": cities})

class MyAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        role = user.userprofile.role
        return Response({'token': token.key, 'role': role})

# Create your views here.
class CommonMachineSettingViewSet(viewsets.ModelViewSet):
    queryset = CommonMachineSetting.objects.all()
    serializer_class = CommonMachineSettingSerializer
class UniqueMachineSettingViewSet(viewsets.ModelViewSet):
    queryset = UniqueMachineSetting.objects.all()
    serializer_class = UniqueMachineSettingSerializer
class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
class MedicineTabletViewSet(viewsets.ModelViewSet):
    queryset = MedicineTablet.objects.all()
    serializer_class = MedicineTabletSerializer
class MedicineOintmentViewSet(viewsets.ModelViewSet):
    queryset = MedicineOintment.objects.all()
    serializer_class = MedicineOintmentSerializer
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
class PatientHistoryPhotosViewSet(viewsets.ModelViewSet):
    queryset = PatientHistoryPhotos.objects.all()
    serializer_class = PatientHistoryPhotosSerializer
class PatientHistoryViewSet(viewsets.ModelViewSet):
    queryset = PatientHistory.objects.all()
    serializer_class = PatientHistorySerializer
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
class PackageCommentViewSet(viewsets.ModelViewSet):
    queryset = PackageComment.objects.all()
    serializer_class = PackageCommentSerializer
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()#.prefetch_related('package_comment')
    serializer_class = PackageSerializer
class DoseCommentViewSet(viewsets.ModelViewSet):
    queryset = DoseComment.objects.all()
    serializer_class = DoseCommentSerializer
class DoseViewSet(viewsets.ModelViewSet):
    queryset = Dose.objects.all()
    serializer_class = DoseSerializer

#Doctor ViewSet storage
class DoctorViewStorageViewSet(viewsets.ModelViewSet):
    queryset = DoctorViewStorage.objects.all()
    serializer_class = DoctorViewStorageSerializer

#Doctor ViewSet
class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    def retrieve(self, request, *args, **kwargs):
        patient = self.get_object()
        patient_history = PatientHistory.objects.filter(patient=patient).first()
        patient_history_photos = []
        if patient_history:
            patient_history_photos = PatientHistoryPhotos.objects.filter(patienthistory=patient_history)

        patient_history_data = {}
        if patient_history:
            patient_history_data = {
                'patient_history_id': str(patient_history.patient_history_id),
                'rating': patient_history.rating,
                'duration': patient_history.duration,
                'activity': patient_history.activity,
                'auto_imm_dis': patient_history.auto_imm_dis,
                'thyroid': patient_history.thyroid,
                'jaundice': patient_history.jaundice,
                'fh_auto_imm_dis': patient_history.fh_auto_imm_dis,
                'ophthalmological_problems': patient_history.ophthalmological_problems,
                'hospitalization': patient_history.hospitalization,
                'psychiatric_history': patient_history.psychiatric_history,
                'keloidol_tendency': patient_history.keloidol_tendency,
                'epilepsy': patient_history.epilepsy,
                'blood_group': patient_history.blood_group,
                'steroid_history': patient_history.steroid_history,
                'antibodies_to_thyroid': patient_history.antibodies_to_thyroid,
                'h_o_epilepsy': patient_history.h_o_epilepsy,
                'fh_b_vitiligo': patient_history.fh_b_vitiligo,
                'h_o_thyroid': patient_history.h_o_thyroid,
                'hb_value': patient_history.hb_value,
                'photo_of_date': [photo.photo.url for photo in patient_history_photos],
            }

        packages = Package.objects.filter(patient_id=patient)
        package_data = []
        for package in packages:
            doses = Dose.objects.filter(package_id=package)
            dose_data = []
            for dose in doses:
                dose_data.append({
                    'dose_id': str(dose.dose_id),
                    'j_cm2': dose.j_cm2,
                    'tube': dose.tube,
                    'status': dose.status,
                })
            package_data.append({
                'package_id': str(package.package_id),
                'package_name': package.package_name,
                'package_status': package.package_status,
                'doses': dose_data,
            })
        data={
            'patient_id': str(patient.patient_id),
            'full_name': patient.full_name,
            'address': patient.city+' '+patient.state+' '+patient.country,
            'dob': patient.date_of_birth,
            'gender':patient.gender,
            'phone_number': patient.phone_number,
            "system_code": patient.system_code,
            "skin_type ":patient.skin_type,
            'registration_date': patient.created_at,
            'patient_history': patient_history_data,
            'packages': package_data,
            'photo': patient.photo.url if patient.photo else None,
        }
        return Response(data)


