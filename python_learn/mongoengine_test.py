from mongoengine import connect
from mongoengine import Document
import mongoengine as Mongo

connect("my_db_test1", host='localhost', port=27017)


class Users(Document):
    name = Mongo.StringField(required=True, max_length=200)
    age = Mongo.IntField(required=True)


# class TestColection(Document):
#     name = Mongo.StringField(required=True, max_length=200)
#     age = Mongo.IntField(required=True)
#     # meta = Mongo.DictField(required=True)
#     meta = {'collection': 'test_collection'}

    # def __init__(self, meta_name):
    #     self.meta = {'collection': meta_name}
    #     print('Hello world')


# a = TestColection(name="zsj2", age=78)
# a.save()
def create_collection_name(cls):
    return "PERSON"


class DynamicPerson(Document):
    name = Mongo.StringField()
    age = Mongo.IntField()

    meta = {'collection': create_collection_name}

for temp in a.objects.all():
    print("name:", temp.name, "age:", temp.age)

Users.objects(name='zsj').update_one(set__age=22)

users = Users.objects.all()
for u in users:
    print("name:", u.name, "age:", u.age)
