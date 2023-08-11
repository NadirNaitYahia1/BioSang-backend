from django.db import models

class Patient(models.Model):
    id_Patient = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.name} {self.prenom}"


class Admin(models.Model):
    id_Admin = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name} "
    

class Ajouter(models.Model): 
    id_ajout = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)    
   
    def __str__(self):
        return f"Ajout {self.patient_id} by {self.admin_id}"

 

class Cliche(models.Model):
    id_Cliche = models.AutoField(primary_key=True)
    ajouter_id = models.ForeignKey(Ajouter, on_delete=models.CASCADE)
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

