from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None     # type: ignore
    first_name = None   # type: ignore
    last_name = None    # type: ignore
    name = CharField(_('name'), max_length=255, blank=True)
    email = EmailField(_('email address'), blank=False, max_length=255, unique=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # type: ignore

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email
