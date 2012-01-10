from mongonaut.sites import MongoAdmin

from entries.models import Post

Post.mongoadmin = MongoAdmin()