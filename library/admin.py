from django.contrib import admin

from .models import CustomUser
from .models import Book

from .models import Author
from .models import Genre
from .models import FileType





# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Book)

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(FileType)



