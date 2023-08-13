from django.db import models
from django.contrib.auth.models import AbstractBaseUser 
class Patient(AbstractBaseUser):
    id_Patient = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey('Admin', on_delete=models.CASCADE)   
    name = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date_naissance = models.DateField()

    USERNAME_FIELD = 'id_Patient'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.name}"


class Admin(AbstractBaseUser):
    id_Admin = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    USERNAME_FIELD = 'id_Admin'
    REQUIRED_FIELDS = []
    def __str__(self):
        return f"{self.name} "
    

 
class Cliche(models.Model):
    id_Cliche = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    cle = models.CharField(max_length=50)
    def __str__(self):
        return f"Cliché {self.id_Cliche} "

class Analyse(models.Model):
    id_analyse = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='uploads/')
    date = models.DateField()
    def __str__(self):
        return f"Analyse {self.id_analyse} by {self.admin_id} for {self.patient_id}"

