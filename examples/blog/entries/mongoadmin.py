from mongonaut.sites import NautSite

from entries.models import Post

NautSite.register(Post)