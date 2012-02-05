from django.conf import settings
from django.utils.importlib import import_module

from django.conf import settings

class AppStore(object):
    
    def __init__(self, module):
        self.models = []
        for key in module.__dict__.keys():
            model_candidate = getattr(module, key)
            if hasattr(model_candidate, 'mongoadmin'):
                self.add_model(model_candidate)
                
    def add_model(self, model):
        model.name = model.__name__
        self.models.append(model)
        
class MongonautViewMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(MongonautViewMixin, self).get_context_data(**kwargs)
        context['MONGONAUT_JQUERY'] = getattr(settings, "MONGONAUT_JQUERY", "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js")
        context['MONGONAUT_TWITTER_BOOTSTRAP'] = getattr(settings, "MONGONAUT_TWITTER_BOOTSTRAP", "http://twitter.github.com/bootstrap/assets/css/bootstrap.css")
        context['MONGONAUT_TWITTER_BOOTSTRAP_ALERT'] = getattr(settings, "MONGONAUT_TWITTER_BOOTSTRAP_ALERT", "http://twitter.github.com/bootstrap/assets/js/bootstrap-alert.js")
        return context
    
    def get_mongoadmins(self):
        """ Returns a list of all mongoadmin implementations for the site """
        apps = []        
        for app_name in settings.INSTALLED_APPS:
            mongoadmin = "{0}.mongoadmin".format(app_name)
            try:
                module = import_module(mongoadmin)
            except ImportError as e:
                if str(e) == "No module named mongoadmin":
                    continue
                raise e
            
            app_store = AppStore(module)
            apps.append(dict(
                app_name=app_name,
                obj=app_store
            ))
        return apps
        
    
    def set_mongonaut_base(self):
        """ Sets a number of commonly used attributes """        
        if hasattr(self, "app_label"):
            # prevents us from calling this multiple times
            return None
        self.app_label = self.kwargs.get('app_label')
        self.document_name = self.kwargs.get('document_name')
    
        # TODO Allow this to be assigned via url variable
        self.models_name = self.kwargs.get('models_name', 'models')
    
        # import the models file
        self.model_name = "{0}.{1}".format(self.app_label, self.models_name)
        self.models = import_module(self.model_name)
        
    def set_mongoadmin(self):
        """ Returns the MongoAdmin object for an app_label/document_name style view
        """
        if hasattr(self, "mongoadmin"):
            return None
                    
        if not hasattr(self, "document_name"):
            self.set_mongonaut_base()
        
        for mongoadmin in self.get_mongoadmins():
            for model in mongoadmin['obj'].models:
                if model.name == self.document_name:
                    self.mongoadmin = model.mongoadmin
                    break
        # TODO change this to use 'finally' or 'else' or something
        if not hasattr(self, "mongoadmin"):
            raise NoMongoAdminSpecified("No MongoAdmin for {0}.{1}".format(self.app_label, self.document_name))

    def set_permissions_in_context(self, context={}):
        """ Provides permissions for mongoadmin for use in the context"""
        
        context['has_view_permission'] = self.mongoadmin.has_view_permission(self.request)
        context['has_edit_permission'] = self.mongoadmin.has_edit_permission(self.request)
        context['has_add_permission'] = self.mongoadmin.has_add_permission(self.request)
        context['has_delete_permission'] = self.mongoadmin.has_delete_permission(self.request)
        return context
            