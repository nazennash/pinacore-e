from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(blank=True, unique=True, null=False, blank=False )
    name = models.CharField(max_length=50)
    otp = models.CharField(max_length=4)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(default=settings.MAX_OTP_TRY, max_length=2)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    user_registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.phone_number
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone_number'
    objects = 'UserManager()'