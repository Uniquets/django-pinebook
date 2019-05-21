from django.contrib import admin
import users.models as user
import book.models as book

admin.site.register(user.School)
admin.site.register(user.Reader)
admin.site.register(user.City)
admin.site.register(book.Book)
admin.site.register(book.Press)
admin.site.register(book.Author)

