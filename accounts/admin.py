from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from accounts.models import *

from accounts.mixin import ReadOnlyAdminMixin


class UserAdmin(DjangoUserAdmin):
    # list_display = ("id",'email','username','phone','phone_verfied',
    list_display = ("id",'username','first_name','last_name','total_points',
    'current_level','date_joined',
    'is_staff','is_active',
    )
    # here in fieldsets we add the fields which users can see in admin panel
    fieldsets = (
        (None, {'fields': ('email','username','password',
        'first_name','last_name','total_points','current_level',
        'is_active',)}),
        # ('Personal info', {'fields': ('',)}),
        # ('Permissions', {'fields': ('',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # this field will be asked when creating a user in admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
            'first_name','last_name','total_points',
            'password1', 'password2','is_staff')}
        ),
    )
    ordering = ('-date_joined',)
    search_fields = ('id','username')
  



class LevelAdmin(admin.ModelAdmin):
    list_display = ['id','name','min_point','max_point']




class ActionAdmin(admin.ModelAdmin):
    list_display = ['id','name','current_point_limit_for_day']



class PointsAdmin(admin.ModelAdmin):
    list_display = ['id','action','level','points']





class ReviewAdmin(admin.ModelAdmin,ReadOnlyAdminMixin):
    list_display = ['id','user','content','points_earned']


class ShortStoryAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
    list_display = ['id','user','content','points_earned']


admin.site.register(User,UserAdmin)
admin.site.register(Level,LevelAdmin)
admin.site.register(Action,ActionAdmin)

admin.site.register(Review,ReviewAdmin)
admin.site.register(ShortStory,ShortStoryAdmin)
admin.site.register(Points,PointsAdmin)
