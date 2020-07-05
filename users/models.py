from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from leagues.models import League


class UserModelManager(BaseUserManager):
    """Required Object Manager for UserAccount"""

    def create_user(self, email, first_name, last_name, password=None):
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""
    leagues = models.ManyToManyField(League, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    email_notifications = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_configured = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, blank=True)
    phone_notifications = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/', null=True, blank=True)
    date_joined = models.DateTimeField(default=now)

    ACCOUNT_TYPE_CHOICES = (
        ('umpire', 'umpire'),
        ('manager', 'manager'),
        ('inactive', 'inactive'),
    )

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='inactive')

    objects = UserModelManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def configure_user(self):
        self.is_configured = True
        self.save()

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class UserLeagueStatus(models.Model):
    """Information relevant to a user for a specific league"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date_pending = models.DateTimeField(default=now)
    date_joined = models.DateTimeField(default=now)

    JOIN_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
    )

    join_status = models.CharField(max_length=10, choices=JOIN_STATUS_CHOICES, default="pending")

    # Umpire Relevant Fields
    max_casts = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def accept_user(self):
        self.join_status = 'accepted'
        self.date_joined = now
        self.save()

    def remove_user(self):
        self.join_status = 'pending'
        self.save()

    def set_max_casts(self, max_casts):
        self.max_casts = max_casts
        self.save()


