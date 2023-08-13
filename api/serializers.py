from rest_framework import serializers
from .models import Patient
from .models import Admin  

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