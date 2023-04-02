from django.db import models

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class AccountManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Users must have an account id")
        if not password:
            raise ValueError("Users must have an password")
        account = self.model(username, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)
    
    
    def __str__(self) -> str:
        return self.country_code

class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True, primary_key=True,db_index=True)
    phone_number = models.CharField(max_length=10, unique=True, blank=False,db_index=True)
    email = models.EmailField(unique=True, blank=False,db_index=True)
    account_number = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=30, blank=True, db_index=True)
    cisf_code = models.CharField(max_length=100, blank=True)
    branch_name = models.CharField(max_length=100, blank=True)
    account_holder_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=300, blank=True)
    education = models.CharField(max_length=200, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['email', 'phone']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def staff(self):
        "Is the user a member of staff?"
        return self.is_satff
    
    


# class Profile(models.Model):
#     # id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
#     creator = models.ForeignKey(Account,on_delete=models.CASCADE)
#     account_number = models.CharField(max_length=100, blank=True)
#     name = models.CharField(max_length=30, blank=True, db_index=True)
#     cisf_code = models.CharField(max_length=100, blank=True)
#     branch_name = models.CharField(max_length=100, blank=True)
#     account_holder_name = models.CharField(max_length=100, blank=True)
#     address = models.CharField(max_length=300, blank=True)
#     education = models.CharField(max_length=200, blank=True)
    


