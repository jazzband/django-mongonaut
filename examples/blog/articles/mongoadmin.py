from mongonaut.sites import MongoAdmin

from articles.models import Post

Post.mongoadmin = MongoAdmin()