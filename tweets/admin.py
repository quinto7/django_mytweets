from django.contrib import admin
from models import Tweet, HashTag
# Register your models here.
admin.site.register(Tweet)  #Para que nuestros models  esten en el Django model
admin.site.register(HashTag)
