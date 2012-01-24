from mongonaut.sites import MongoAdmin

from articles.models import Post, User

class PostAdmin(MongoAdmin):
    
    def has_view_permission(self, request):
        return True

    def has_edit_permission(self, request):
        return True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request):
        return True


    search_fields = ('title',)


Post.mongoadmin = PostAdmin()
User.mongoadmin = MongoAdmin()