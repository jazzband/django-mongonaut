from mongoengine.base import ObjectIdField, ValidationError

# Used to valid object_ids.
# Called by is_valid_object_id
OBJECT_ID = ObjectIdField()

def is_valid_object_id(value):
    try:
        OBJECT_ID.validate(value)
        return True
    except ValidationError:
        return False
