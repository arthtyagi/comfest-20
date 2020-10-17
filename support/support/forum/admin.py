from forum.models import Query
from django.contrib import admin
from .models import *

admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(Comment)
