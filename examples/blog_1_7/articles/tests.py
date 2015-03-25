import uuid
from django.test import TestCase
from mongoengine import connect, errors
from mongonaut.forms import MongoModelForm
from blog_1_7.settings import MONGO_DATABASE_NAME
from articles.models import User, Comment, Post, OrderedUser


class PostAndUserTestCase(TestCase):
    def setUp(self):
        uid = uuid.uuid4().hex
        self.author = User.objects.create(
            email='{0}@test.com'.format(uid),
            first_name='test',
            last_name='user'
        )
        self.comment = Comment(
            message='Default test embedded comment',
            author=self.author
        )
        self.post = Post(
            title='Test Article {0}'.format(uid),
            content='I am test content',
            author=self.author,
            published=True,
            tags=['post', 'user', 'test'],
            comments=[self.comment]
        )

    def tearDown(self):
        conn = connect(MONGO_DATABASE_NAME)
        conn.drop_database(MONGO_DATABASE_NAME)
        # To reserve database but remove test data
        #db = conn[MONGO_DATABASE_NAME]
        #db.post.remove({'title': self.post.title})
        #db.user.remove({'email': self.author.email})

    def test_user_required_field(self):
        invalid_author = User(first_name='test', last_name='user')
        self.assertRaises(errors.ValidationError, invalid_author.save)

    def test_post_save_method(self):
        self.post.save()
        self.assertEquals(self.post.creator.email, self.author.email)


class FormMixinsGetFormFieldDictTestCase(TestCase):
    def setUp(self):
        uid = uuid.uuid4().hex
        self.author = User(
            email='{0}@test.com'.format(uid),
            first_name='test',
            last_name='user'
        )

    def test_form_fields_default_sort_ordering(self):
        # At default, the form fields will be ordered by python sorted()
        my_form = MongoModelForm(None, model=User, instance=self.author).get_form()
        field_names = [field.name for field in my_form]
        self.assertEquals(field_names, ['email', 'first_name', 'id', 'last_name'])

    def test_form_fields_ordering_inherit_from_model_meta_class(self):
        # if form_fields_ordering is set under model's Meta class,
        # ordering will be prioritized, then remaining fields are sorted
        ordered_author = OrderedUser(
            email=self.author.email,
            first_name=self.author.first_name,
            last_name=self.author.last_name
        )
        my_form = MongoModelForm(None, model=OrderedUser, instance=ordered_author).get_form()
        field_names = [field.name for field in my_form]
        self.assertEquals(field_names, ['first_name', 'last_name', 'email', 'id'])

