#!/usr/bin/python3
""" Database Storage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the class """
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(user,
                                                              password,
                                                              host,
                                                              database),
                                                       pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns all the objects of a specific class """
        classes = [State, City, User, Place, Review, Amenity]
        dictionary = {}
        objects = []
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            objects = self.__session.query(cls).all()
        else:
            for a_class in classes:
                objects.extend(self.__session.query(a_class).all())

        for item in objects:
            key = "{}.{}".format(type(item).__name__, item.id)
            dictionary[key] = item
        return dictionary

    def new(self, obj):
        """ Adds a new object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Saves the changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes obj from the current session. """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all the tables in the database """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit = False)
        Session = scoped_session(session_factory)
        self.__session = Session()
