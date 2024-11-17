from django.db import models


# Create your models here.
class CitizenParent(models.Model):
    citizen_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)


class Citizen(models.Model):
    citizen_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)


class Colline(models.Model):
    name = models.CharField(max_length=30)


class Commune(models.Model):
    name = models.CharField(max_length=30)


class IdCardRegistration(models.Model):
    citizen_id = models.IntegerField()


class LostIdCardReport(models.Model):
    citizen_id = models.IntegerField()


class Province(models.Model):
    name = models.CharField(max_length=30)


class Publication(models.Model):
    pub_id = models.IntegerField()
    title = models.CharField(max_length=20)
    files = models.CharField(max_length=50)
    pub_date = models.DateField(auto_now=False, auto_now_add=False)


class RegisteredIdCard(models.Model):
    citizen_id = models.IntegerField()


class RegisteredIdCardApplication(models.Model):
    citizen_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    email = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    picture = models.ImageField(upload_to="applicants/")
    residence = models.CharField(max_length=50)


class Service(models.Model):
    name = models.CharField(max_length=20)
