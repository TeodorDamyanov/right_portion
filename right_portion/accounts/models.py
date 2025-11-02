from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import gettext_lazy as _

# Create your models here.


def only_alpha_validator(value):
    if not value.isalpha():
        raise ValidationError('Name must include only letters!')


class RPUser(auth_models.AbstractUser):
    NAMES_MIN_LENGTH = 2
    NAMES_MAX_LENGTH = 30

    username = models.CharField(
        max_length=NAMES_MAX_LENGTH,
        help_text="",
        unique=True,
        validators=(validators.MinLengthValidator(NAMES_MIN_LENGTH), only_alpha_validator,)
    )

    email = models.EmailField(
        unique=True,
    )

    profile_picture = models.ImageField(
        null=True,
        blank=True,
    )

    is_employee = models.BooleanField(
        _("employee status"),
        default=False,
    )
