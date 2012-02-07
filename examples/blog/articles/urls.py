from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from articles.models import Post

urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=ListView.as_view(
            queryset=Post.objects.all(),
            template_name="articles/post_list.html"
        ),
        name="article_list"
    ),
)
