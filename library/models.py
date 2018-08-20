from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.conf import settings
#from django.core.urlresolvers import reverse
from django.db.models import F
from mybooks.settings import ALLOWED_HOSTS
from pytz import unicode


from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.mail import send_mail





class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(default='')
    @property
    def full_name(self):
        """
        Return the first_name plus the last_name.
        """
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    @property
    def email(self, subject, message, from_email=None, **kwards):
        """
        Sends  an  email to  this author.
        """
        send_mail(subject, message, from_email, [self.email], **kwards)

    def __unicode__(self):
        return unicode(self.first_name, self.last_name)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Author'



class Genre(models.Model):
    genre_name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.genre_name)

    def __str__(self):
        return f'{self.genre_name}'

    def __repr__(self):
        return f'{self.genre_name}'

    class Meta:
        verbose_name = 'Genre'


class FileType(models.Model):
    file_type = models.CharField(max_length=10)

    def __unicode__(self):
        return unicode(self.file_type)

    def __str__(self):
        return f'{self.file_type}'

    def __repr__(self):
        return f'{self.file_type}'

    class Meta:
        verbose_name = 'File Type'


class Book(models.Model):
    title = models.CharField(max_length=200)
    init_title = models.CharField(max_length=200)
    pages = models.IntegerField(default=0)
    published_year = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(default='title')
    genre = models.ManyToManyField(Genre)
    author = models.ManyToManyField(Author)
    file_type = models.ForeignKey(FileType)

    types = (
        ('English', 'English'),
        ('Russian', 'Russian'),
        ('Other', 'Other')
    )
    language = models.CharField(max_length=50, choices=types, default='Other')

    publisher = models.CharField(max_length=100, null=True, blank=True)
    stars = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(default='')
    img = models.ImageField(upload_to='photos/', null=True, blank=True)
    file = models.FileField(upload_to='file_storage/',  null=True, blank=True)

    def __unicode__ (self):
        return unicode(self.title)

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Book'


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    email = models.EmailField(
        _('Email Address'), unique = True,
        error_messages = {
            'unique': _("A user with that email already exists."),
        }
    )

    username = models.CharField(_('username'), max_length=30, unique=True, blank=True, null=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _('A user with that username already exists.'),

                                }

                                )

    first_name = models.CharField(_('first name'), max_length = 30, blank=True)
    last_name = models.CharField(_('last name'), max_length = 30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))

    objects = UserManager()

    timezone = models.CharField(max_length=50, default='Europe/Moscow')
    registration_date = models.DateTimeField(auto_now_add=True, blank=True)  # time

    headshot = models.ImageField(upload_to='photos/', null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return '{}'.format(self.username)

    def __str__(self):
        return '{}'.format(self.username)

    def __repr__(self):
        return '{}'.format(self.username)


    def get_full_name(self):
        """
        Return the first_name plus the last_name, with the space in between.
        """
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

