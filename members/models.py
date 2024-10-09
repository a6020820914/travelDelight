from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.conf import settings

class MemberManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('用户必须有一个邮箱地址')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)  # 额外字段
    location = models.CharField(max_length=30, blank=True)  # 额外字段
    birth_date = models.DateField(null=True, blank=True)  # 额外字段
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    # 使用related_name区分不同模型之间的groups和user_permissions字段
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='member_set',  # 改变related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='member_set',  # 改变related_name
        blank=True
    )

class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # 删除头像文件
        if self.avatar:
            self.avatar.delete(save=False)  # 只删除文件，不保存模型
        super().delete(*args, **kwargs)  # 删除模型实例

# 如果您需要 CustomUser ，可以将其定义如下：
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/image.png')

    # 同样使用related_name区分
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',  # 改变related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_set',  # 改变related_name
        blank=True
    )

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name