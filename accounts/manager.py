from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import re

PHONE_REGEX = r"(^923[0-9]{9})"


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a User with the given phone and password.
        """
        if not phone:
            raise ValueError(_('Phone number must be set'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given pone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone, password, **extra_fields)


    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if self.validate_phone(phone) == '1':
            return self.create_user(phone, password, **extra_fields)
        else:
            raise ValueError(_('Phone number must be 923xxxxxxxxx format'))

    def validate_phone(self, phone):
        try:
            """
            formats the mobile number in correct form
            """
            if phone and not re.fullmatch(PHONE_REGEX, phone):
                return str(0)
            else:
                return str(1)
        except:
            raise ValueError(
                _("An error occured while validating format of phone no: "))
