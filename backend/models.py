from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

# Create your models here.
# This section code all the model for the database
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_Id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    username = models.EmailField(max_length=100, null=False, unique=True)
    profile_name = models.CharField(max_length=20, null=False)
    user_Profile = models.FileField(upload_to='User-Profile/', null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_Created = models.DateTimeField(null=False, auto_now_add=True)
    failed_login_attempts = models.IntegerField(default=0)
    lockout_timestamp = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def increment_failed_login_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 3:
            # Lock the account for 5 minutes
            self.lockout_timestamp = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.lockout_timestamp = None
        self.save()

    class Meta:
        db_table = 'User'

class Anime(models.Model):
    anime_Id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    user_Id = models.ForeignKey(User, null=False, editable=False, on_delete=models.RESTRICT, db_column='user_Id')
    anime_Number = models.CharField(max_length=10, null=False)
    anime_Name = models.CharField(max_length=100, null=False)
    anime_Picture = models.URLField(null=False)
    anime_Status = models.CharField(max_length=15, null=False)
    class Meta:
        db_table = 'Anime'

class AnimeEpisode(models.Model):
    episode_Id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    anime_Id = models.ForeignKey(Anime, null=False, editable=False, on_delete=models.RESTRICT, db_column='anime_Id')
    episode_Number = models.IntegerField(null=False)
    episode_Name = models.CharField(max_length=200, null=False)
    episode_Status = models.CharField(max_length=15, null=False)
    class Meta:
        db_table = 'Anime Episode'