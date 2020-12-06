from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, type, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.create(
                email=self.normalize_email(email),
                username=username,
                type=type

            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, type, password):
        user = self.create(
            email=self.normalize_email(email),
            username=username,
            password=password,
            type=type
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        PLAYER = "PLAYER", "Player"
        COACH = "COACH", "Coach"

    type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.PLAYER)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'type']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True




# class User(AbstractUser):
#     class Types(models.TextChoices):
#         PLAYER = "PLAYER", "Player"
#         COACH = "COACH", "Coach"
#
#     type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.PLAYER)
#
#     name = models.CharField(_("Name of User"), blank=True, max_length=255)
#
    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username": self.username})
#
#
class PlayerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PLAYER)


class CoachManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.COACH)


class Player(User):
    base_type = User.Types.PLAYER
    objects = PlayerManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.playermore

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.PLAYER
        return super().save(*args, **kwargs)


class PlayerMore(models.Model):
    def __str__(self):
        return self.name
    player = User.objects.latest('date_joined')
    trial = User.objects.all().last()
    email = trial.email

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=player)
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=2000, default='https://ih1.redbubble.net/image.702995522.8412/flat,750x,'
                                                      '075,f-pad,750x1000,f8f8f8.jpg')
    age = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    club = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    gradyear = models.CharField(max_length=200)
    gpa = models.CharField(max_length=200)
    height = models.CharField(max_length=200, default='')
    weight = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default=player)
    phone = models.CharField(max_length=200)
    summary = models.TextField(max_length=2000, default='')
    skills = models.TextField(max_length=2000, default='')
    highlight = models.FileField(upload_to='post_files', blank=True, null=True, default='')


class CoachMore(models.Model):
    def __str__(self):
        return self.name
    coach = User.objects.latest('date_joined')

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=coach)
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=2000, default='https://st2.depositphotos.com/1338217/6803/v/950/depositphotos'
                                                      '_68039059-stock-illustration-soccer-coach-with-ball.jpg')
    state = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    experience = models.TextField(max_length=2000)
    email = models.CharField(max_length=200 , default=coach)
    phone = models.CharField(max_length=200)
    requirements = models.TextField(max_length=2000)


class Coach(User):
    base_type = User.Types.COACH
    objects = CoachManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.coachmore

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.COACH
        return super().save(*args, **kwargs)


class Contact(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    email = models.EmailField()
    age = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
