from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from users.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    img = models.ImageField(verbose_name="Картинка", upload_to="image/%Y", null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

#----------------------------------------------------------------------

# class AppUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Требуется Email")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_superuser(self, email, username, password=None, **extra_fields):
#         user = self.create_user(email, username, password, **extra_fields)

#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user


# class AppUser(AbstractBaseUser, PermissionsMixin):
#     user_id = models.AutoField(primary_key=True)
#     email = models.EmailField(max_length=50, unique=True)
#     username = models.CharField(max_length=50)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = AppUserManager()
#     def __str__(self):
#         return self.username
