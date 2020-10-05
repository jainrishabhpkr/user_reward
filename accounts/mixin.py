

class ReadOnlyAdminMixin(object):
    


    def has_change_permission(self, request, obj=None):
        
        return True
        

    def has_add_permission(self, request):
        return True


    def has_delete_permission(self, request, obj=None):
        return True
