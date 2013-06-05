from django.conf.urls import patterns, url


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
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/add/$',
        view=views.DocumentAddFormView.as_view(),
        name="document_detail_add_form"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/(?P<id>[\w]+)/$',
        view=views.DocumentDetailView.as_view(),
        name="document_detail"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/(?P<id>[\w]+)/edit/$',
        view=views.DocumentEditFormView.as_view(),
        name="document_detail_edit_form"
    ),
    url(
        regex=r'^(?P<app_label>[_\-\w]+)/(?P<document_name>[_\-\w]+)/(?P<id>[\w]+)/delete/$',
        view=views.DocumentDeleteView.as_view(),
        name="document_delete"
    )
)
