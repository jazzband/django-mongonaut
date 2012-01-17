from mongonaut.sites import MongoAdmin

from articles.models import Post, User

class PostAdmin(MongoAdmin):
    
    def has_permission(self, request):
        return True

    def has_staff_permission(self, request):
        return True



Post.mongoadmin = PostAdmin()
User.mongoadmin = MongoAdmin()