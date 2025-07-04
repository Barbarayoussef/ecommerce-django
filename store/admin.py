from django.contrib import admin
from .models import Customer,Order,Product,Profile
from django.contrib.auth.models import User

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)


#mi profile info and user info
class ProfileInLine(admin.StackedInline):
    model=Profile

#extend user Model
class UserAdmin(admin.ModelAdmin):
    model= User
    field=['username','first_name','last_name','email']
    inlines=[ProfileInLine]

#unregister the old way
admin.site.unregister(User)

#re-register the new way
admin.site.register(User,UserAdmin) 
