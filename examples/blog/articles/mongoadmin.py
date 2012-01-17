from mongonaut.sites import MongoAdmin

from articles.models import Post, User

Post.mongoadmin = MongoAdmin()
User.mongoadmin = MongoAdmin()