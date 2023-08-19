from rest_framework import serializers
from .models import Patient
from .models import Admin 
from .models import Analyse 
 

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id_Patient', 'name', 'prenom', 'password', 'date_naissance']

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  
        instance.save()
        return instance
    

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id_Admin', 'name', 'password']


    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  
        instance.save()
        return instance
    
class AnalyseSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    admin_id = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.all())

    class Meta:
        model = Analyse
        fields = ['id_analyse','patient_id','admin_id' , 'fichier', 'date']


 