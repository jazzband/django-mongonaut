from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^mongonaut/', include('mongonaut.urls')),
    url(r'^', include('articles.urls')),    
)
