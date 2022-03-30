from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.html import format_html


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=120, verbose_name='نام')
    last_name = models.CharField(max_length=120, verbose_name='نام خانوادگی')
    username = models.CharField(max_length=120, unique=True, verbose_name='نام کاربری')
    email = models.EmailField(max_length=120, null=True, blank=True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=120, unique=True, verbose_name='شماره همراه')
    date_join = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')
    last_login = models.DateTimeField(auto_now_add=True, verbose_name='اخرین ورود')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    class Meta:
        verbose_name = 'حساب های کاربران'
        verbose_name_plural = 'حساب های کاربران'


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='کاربر')
    address_line1 = models.CharField(blank=True, max_length=100, null=True, verbose_name='آدرس اول ')
    profile_picture = models.ImageField(blank=True, null=True, upload_to='photos/userprofile',
                                        verbose_name='تصویر کاربر',
                                        default='photos/userprofile/user.png')
    city = models.CharField(blank=True, null=True, max_length=20, verbose_name='شهر')
    state = models.CharField(blank=True, null=True, max_length=20, verbose_name='کوچه')
    country = models.CharField(blank=True, null=True, max_length=20, verbose_name='کشور')

    def __str__(self):
        return self.user.first_name

    def img(self):
        return format_html('<img src="{}" height="50" style="border-radius:50px;"/>'.format(self.profile_picture.url))

    class Meta:
        verbose_name = 'پروفایل کاربران'
        verbose_name_plural = 'پروفایل کاربران'
