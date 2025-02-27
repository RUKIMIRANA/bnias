import random
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_random_card_id():
    return random.randint(10000000, 99999999)


# Create your models here.
class Profile(models.Model):
    bio = models.TextField()
    profile_user_id = models.BigIntegerField()
    image = models.ImageField(upload_to="profiles", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username  # type: ignore


class Citizen(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    phone = models.IntegerField()
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mother = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_of_mother"
    )
    father = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="child_of_father"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Province(models.Model):
    name = models.CharField(max_length=30)
    head = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Commune(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    chief = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.province.name} -> {self.name}"


class Colline(models.Model):
    name = models.CharField(max_length=30)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)
    chief = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.commune.province.name} -> {self.commune.name} -> {self.name}"


class LostIdCardReport(models.Model):
    card_id = models.IntegerField(null=True)
    report = models.TextField(null=True)
    date = models.DateField(auto_now=True)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)
    colline = models.ForeignKey(Colline, on_delete=models.CASCADE, null=True)


class Publication(models.Model):
    title = models.CharField(max_length=20)
    files = models.FileField(upload_to="publication/")
    pub_date = models.DateField(auto_now=False, auto_now_add=False)


class RegisteredIdCardApplication(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    picture = models.ImageField(upload_to="applicants/")
    residence = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True)
    colline = models.ForeignKey(Colline, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class RegisteredIdCard(models.Model):
    card_id = models.IntegerField(default=generate_random_card_id)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True)
    applicant = models.ForeignKey(
        RegisteredIdCardApplication, on_delete=models.CASCADE, null=True
    )


class Service(models.Model):
    name = models.CharField(max_length=20)
    requirement = models.TextField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    message = models.TextField()
    url = models.CharField(max_length=255, default="#")
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.message}"
