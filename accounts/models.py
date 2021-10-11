from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email'))
        if not first_name:
            raise ValueError(_('You must provide a first name'))
        if not last_name:
            raise ValueError(_('You must provide a last name'))
        if not password:
            raise ValueError(_('You must provide a password'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email'))
        if not first_name:
            raise ValueError(_('You must provide a first name'))
        if not last_name:
            raise ValueError(_('You must provide a last name'))
        if not password:
            raise ValueError(_('You must provide a password'))
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                _('Superuser must be assigned to is_superuser=True'))
        if other_fields.get("is_active") is not True:
            raise ValueError(_('Superuser must be assigned to is_active=True'))
        return self.create_user(email, first_name, last_name, password, **other_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return str(self.email)
