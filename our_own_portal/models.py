from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Student"), (3, "Company"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    '''name = models.CharField(max_length=40)'''
    objects = models.Manager()


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    college_id = models.IntegerField(default=1)
    college_name = models.CharField(max_length=50)
    college_degree = models.CharField(max_length=50)
    cgpa = models.DecimalField(decimal_places=2, max_digits=4, default=1)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin_code = models.IntegerField(default=1)
    contact_no = models.BigIntegerField(default=1)
    dob = models.DateField(default="2001-01-01")
    gender = models.CharField(max_length=10, default=1)
    skills = models.TextField(default="")
    objects = models.Manager()


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50)
    admin = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    sector = models.CharField(max_length=20)
    world_rank = models.IntegerField(default=1)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin_code = models.IntegerField(default=1)
    contact_no = models.BigIntegerField(default=1)
    mode = models.CharField(max_length=30)
    weekly_off = models.TextField(default="Sunday")
    working_hours = models.IntegerField(default=1)
    sick_leaves = models.IntegerField(default=1)
    revenue = models.IntegerField(default=1)
    objects = models.Manager()


class Job(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=30)
    vacancy = models.IntegerField(default=1)
    experience_level = models.CharField(max_length=20)
    min_salary_LPA = models.DecimalField(decimal_places=2, max_digits=4, default=1.0)
    avg_salary_LPA = models.DecimalField(decimal_places=2, max_digits=4, default=1.0)
    max_salary_LPA = models.DecimalField(decimal_places=2, max_digits=4, default=1.0)
    required_skills = models.TextField()
    objects = models.Manager()


class AppliedStudent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default="")
    objects = models.Manager()


class SelectedStudent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    mode = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Student.objects.create(admin=instance, college_id=1, cgpa=1, pin_code=1, contact_no=1, dob="2001-01-01")
        if instance.user_type == 3:
            Company.objects.create(admin=instance, world_rank=1, pin_code=1, contact_no=1, weekly_off="Sunday", revenue=1, working_hours=1)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.student.save()
    if instance.user_type == 3:
        instance.company.save()
