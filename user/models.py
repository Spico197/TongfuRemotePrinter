from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given stu_id must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class LabUser(AbstractUser):
    stu_id = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=200, default='李大嘴', null=True, blank=True)
    memo = models.TextField(default='同福客栈掌勺', null=True, blank=True)

    REQUIRED_FIELDS = ['stu_id']
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class UserPrintRecord(models.Model):
    user = models.ForeignKey(LabUser, on_delete=models.SET_NULL, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=1000)

    class Meta:
        verbose_name = '用户打印记录'
        verbose_name_plural = verbose_name
