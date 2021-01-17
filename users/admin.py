from django.contrib import admin
from items.models import *
from users.models import *
from reviews.models import *

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Review)
