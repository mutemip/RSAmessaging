from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomeUserManager(BaseUserManager):
    def create_user(self, email, password, firstname, public_key):
        user = self.model(email=email, password=password, public_key=public_key, firstname=firstname)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, firstname, public_key):
        user = self.create_user(email=email, password=password, public_key=public_key, firstname=firstname)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomeUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    public_key = models.CharField(max_length=2000, default="null")
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['firstname', 'public_key']
    USERNAME_FIELD = 'email'

    objects = CustomeUserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email


class Messages(models.Model):
    sender = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    Message = models.CharField(max_length=1000)

    def __str__(self):
        return self.sender.email
