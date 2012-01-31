from django.conf.urls.defaults import patterns, url
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from mongonaut import views

urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name="index"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/$',
        view=views.DocumentListView.as_view(),
        name="document_list"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/(?P<id>[\w]{24})/$',
        view=views.DocumentDetailView.as_view(),
        name="document_detail"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/(?P<id>[\w]{24})/edit/$',
        view=views.DocumentDetailEditFormView.as_view(),
        name="document_detail_edit_form"
    ),    
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/add/$',
        view=views.DocumentDetailAddFormView.as_view(),
        name="document_detail_add_form"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/(?P<id>[\w]{24})/delete/$',
        view=views.DocumentDeleteView.as_view(),
        name="document_delete"
    )    
)


