from django.views.generic import ListView

from articles.models import Post


class PostListView(ListView):
    
    template_name="articles/post_list.html"
    
    def get_queryset(self):
        
        return Post.objects.all()
