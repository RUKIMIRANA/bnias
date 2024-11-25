from django.db import models


# Create your models here.
class CitizenParent(models.Model):
    citizen_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Citizen(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    phone_number = models.IntegerField()
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Province(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Commune(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.province.name + " -> " + self.name


class Colline(models.Model):
    name = models.CharField(max_length=30)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.commune.name + " -> " + self.name


class IdCardRegistration(models.Model):
    citizen_id = models.IntegerField()


class LostIdCardReport(models.Model):
    citizen_id = models.IntegerField()


class Publication(models.Model):
    title = models.CharField(max_length=20)
    files = models.FileField(upload_to="publication/")
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

    def __str__(self):
        return self.first_name + " " + self.last_name


class Service(models.Model):
    name = models.CharField(max_length=20)
    requirement = models.TextField()

    def __str__(self):
        return self.name
