class MissingPreliminaryMethod(Exception):
    """ Thrown when a preliminary method is not called. """
    pass

class NoMongoAdminSpecified(Exception):
    """ Called when no MongoAdmin is specified. Unlike to ever be called."""
    pass