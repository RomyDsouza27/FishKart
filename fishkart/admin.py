from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from fishkart.models import Fishlist,Customer,Restaurant,User, Orders, Cart


class UserAdmin(admin.ModelAdmin):
	model = User
	filter_horizontal = ('user_permissions', 'groups',)
admin.site.register(User, UserAdmin)
admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Fishlist)
admin.site.register(Orders)
admin.site.register(Cart)
