#import re
#import sys

from django.conf import settings
from django import http
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.functional import update_wrapper
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from mongoengine.base import TopLevelDocumentMetaclass

from mongonaut.options import ModelAdmin

LOGIN_FORM_KEY = 'this_is_the_login_form'

class NautSite(object):
    """
    A NautSite object encapsulates an instance of the mongonaut application, ready
    to be hooked in to your URLconf. Models are registered with the mongonaut using the
    register() method, and the get_urls() method can then be used to access Django view
    functions that present a full admin interface for the collection of registered
    models.
    """
    login_form = None
    index_template = None
    app_index_template = None
    _registry = {}

    def __init__(self, name=None, app_name='admin'):
        self._registry = {} # model_class class -> admin_class instance
        self.root_path = None
        if name is None:
            self.name = 'admin'
        else:
            self.name = name
        self.app_name = app_name

    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Registers the given model(s) with the given mongonaut class.

        The model(s) should be Model classes, not instances.

        If an mongonaut class isn't given, it will use ModelAdmin (the default
        admin options). If keyword arguments are given -- e.g., list_display --
        they'll be applied as options to the admin class.

        If a model is already registered, this will raise AlreadyRegistered.

        If a model is abstract, this will raise ImproperlyConfigured.
        """
        
        if not admin_class:
            admin_class = ModelAdmin
            
        if isinstance(model_or_iterable, TopLevelDocumentMetaclass):
            model_or_iterable = [model_or_iterable]
            
        for model in model_or_iterable:            
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)
                
                if options:
                    # For reasons I don't quite understand, without a __module__
                    # the created class appears to "live" in the wrong place,
                    # which causes issues later on.
                    options['__module__'] = __name__
                    admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)                

        # Instantiate the admin class to save in the registry
        self._registry[model] = admin_class(model, self)

    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]
            
    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include

        #if settings.DEBUG:
        #    self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)
            
        # Admin-site-wide views.
        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.index),
                name='index'),
            url(r'^(?P<app_label>\w+)/$',
                wrap(self.app_index),
                name='app_list')
        )
        # Add in each model's views.
        for model, model_admin in self._registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.module_name),
                    include(model_admin.urls))
            )
        print urlpatterns
        return urlpatterns        
            
    def admin_view(self, view, cacheable=False):
        """
        Decorator to create an admin view attached to this ``AdminSite``. This
        wraps the view and provides permission checking by calling
        ``self.has_permission``.

        You'll want to use this from within ``AdminSite.get_urls()``:

            class MyAdminSite(AdminSite):

                def get_urls(self):
                    from django.conf.urls import patterns, url

                    urls = super(MyAdminSite, self).get_urls()
                    urls += patterns('',
                        url(r'^my_view/$', self.admin_view(some_view))
                    )
                    return urls

        By default, admin_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.
        """
        def inner(request, *args, **kwargs):
            # TODO create new login/permissions scheme similiar to this
            #if not self.has_permission(request):
            #    return self.login(request)
            return view(request, *args, **kwargs)
        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)            
        
    @never_cache
    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        from mongonaut.views import IndexView
        return IndexView
            
    def app_index(self, request, app_label, extra_context=None):
        user = request.user
        has_module_perms = user.has_module_perms(app_label)
        app_dict = {}
        for model, model_admin in self._registry.items():            
            pass

# This global object represents the default admin site, for the common case.
# You can instantiate AdminSite in your own code to create a custom admin site.
site = NautSite()