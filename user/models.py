from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    is_attendant = models.BooleanField(
        default=False,
        help_text='Designates whether the user is attendant.',
    )

    is_operator = models.BooleanField(
        default=False,
        help_text='Designates whether the user is operator.',
    )

    def __str__(self) -> str:
        return self.get_full_name()


class Operator(models.Model):

    operator_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.operator_user.get_full_name()


class Attendant(models.Model):

    attendant_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.attendant_user.get_full_name()
