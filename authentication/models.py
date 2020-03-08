from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.validators import RegexValidator
from utils.managers import CustomQuerySet


# Create your models here.

class UserManager(BaseUserManager):
    # We are overiding the `create_user` method so that users can
    # only be created when all non-nullable fields are populated.

    def create_user(
        self,
        first_name=None,
        last_name=None,
        user_name=None,
        email=None,
        phone_number=None,
        password=None,
        role='NU'
    ):
        # Create and return a `User` with a phone number, first name, last name and
        # password.

        if not first_name:
            raise TypeError('Please provide your First name.')

        if not last_name:
            raise TypeError('Please provide your Last name.')

        if not user_name:
            raise TypeError('Please provide your User name.')

        if not email:
            raise TypeError('Please provide your Email.')

        if not phone_number:
            raise TypeError('Please provide your Phone number')

        if not password:
            raise TypeError('Please secure your account with a password')

        user = self.model(
            email=email, user_name=user_name, phone_number=phone_number
        )

        user.set_password(password)
        user.role = role
        user.is_verified = True
        user.save()
        return user

    def create_superuser(
            self,
            user_name=None,
            email=None,
            password=None):
        # Create a superuser
        if not email:
            raise TypeError('Superusers must have an email.')

        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.model(
            user_name=user_name, email=email, role='FA')

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    # Custom user model

    ROLES = (
        ('FA', 'FREELANCER ADMIN'),
        ('CA', 'COMPANY ADMIN'),
        ('NU', 'NORMAL USER'),
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$',
                                 message='Phone number must be in international format: `+256123456789`.')

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    user_name = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=16, validators=[phone_regex], unique=True, default=False)
    role = models.CharField(verbose_name='user role', max_length=2, choices=ROLES, default='NU')
    is_verified = models.BooleanField(default=False)
    is_company = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        return f'{self.email}'

    @property
    def get_email(self):
        # This method is required by Django for handling emails.
        # Typically, this would be the user's first and last name. Since we do
        # not store the user's real name, we return their email instead.
        return self.email

    @property
    def token(self):
        # We need to make the method for creating our token private. At the
        # same time, it's more convenient for us to access our token with
        # `user.token` and so we make the token a dynamic property by wrapping
        # in in the `@property` decorator.
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """We generate JWT token and add the user id, email,
        user_name, user role and expiration as an integer.
        """
        token_expiry = datetime.now() + timedelta(hours=24)
        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'user_name': self.user_name,
            'role': self.role,
            'exp': token_expiry.utcfromtimestamp(token_expiry.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
