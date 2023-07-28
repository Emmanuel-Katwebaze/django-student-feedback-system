from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
 


class StudentManager(BaseUserManager):
    def create_user(self, **extra_fields):
        student = self.model(**extra_fields)
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    student_id = models.BigIntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    enrollment_year = models.PositiveIntegerField()

    # New field for password storage
    password = models.CharField(max_length=128, default=make_password('12345678'))

    # Set the manager for the custom User model
    objects = StudentManager()

    # Use the student_id as the unique identifier for authentication
    USERNAME_FIELD = 'student_id'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def check_password(self, raw_password):
        # Compare the provided raw_password with the stored password hash
        return check_password(raw_password, self.password)
