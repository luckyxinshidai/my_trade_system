from mongoengine import connect
from mongoengine import Document
import mongoengine as Mongo
import unittest

connect("my_db_test1", host='localhost', port=27017)


class MyCollection():
    name = 123
    age = 456

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def test_collection_name(self):
        def create_collection_name(cls):
            return str(self.age) + str(self.age)

        class DynamicPerson(Document):
            name = Mongo.StringField()
            age = Mongo.IntField()
            meta = {'collection': create_collection_name}

        # collection = DynamicPerson(name='22', age=33)._get_collection_name()
        # print(collection)
        return DynamicPerson(name='123', age=456)


a = MyCollection(name=1113, age=1114)
b = a.test_collection_name()
b.save()
c = MyCollection(name=789, age=1112)
d = c.test_collection_name()
d.save()


