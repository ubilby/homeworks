from abc import ABCMeta, abstractmethod #модуль abc - существует для создания абстрактных классов
#ABCMeta - для наследования при создании абстрактного класса
#abstractmethod - для создания абстрактного метода (метода, без которого нельзя не описать, наследуясь от абстрактного класса)
import os
import pickle
import json


class ParamHandlerException(BaseException):
    pass


class ParamHandler(metaclass=ABCMeta): #создаем абстрактный класс
    def __init__(self, source):
        self.source = source
        self.params = {}


    def add_param(self, key, value):
        self.params[key] = value


    def get_all_params(self):
        return self.params


    @abstractmethod #помечаем метод как абстрактный
    def read(self):
         pass


    @abstractmethod
    def write(self):
        pass


    types = {}


    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ParamHandlerException('Type must have a name!')

        if not issubclass(klass, ParamHandler):
            raise ParamHandlerException('Class "{}" is not ParamHandler!'.format(klass))
        
        cls.types[name] = klass


    @classmethod
    def get_instance(cls, source, *args, **kwargs):
        # Шаблон "Factory Method"
        _, ext = os.path.splitext(str(source).lower())
        ext = ext.lstrip('.')
        klass = cls.types.get(ext)

        if klass is None:
            raise ParamHandlerException('Type "{}" not found!'.format(ext))

        return klass(source, *args, **kwargs)


class TextParamHandler(ParamHandler):
    def read(self):
        """
        Чтение из текстового файла и присвоение значений в self.params
        """
        pass


    def write(self):
        """
        Запись в текстовый файл параметров self.params
        """
        pass
    

class XmlParamHandler(ParamHandler):
    def read(self):
        """
        Чтение в формате XML и присвоение значений в self.params
        """
        pass


    def write(self):
        """
        Запись в формате XML параметров self.params
        """
        pass


class JsonParamHandler(ParamHandler):
    def read(self, name):
        """
        Чтение в формате JSON и присвоение значений в self.params
        """
        with open(name) as f: #json любит словари, все ключи - обязательно в кавычках, нет None, но есть Null
            print("\nДанные прочитаны из json файла: {}\n".format(json.load(f)))


    def write(self, name):
        """
        Запись в формате JSON параметров self.params
        """
        with open(name, "w") as f:      #только в режиме перезаписи
            json.dump(self.params, f)


class PickleParamHandler(ParamHandler):
    def read(self, name):
        """
        Чтение в формате pickle и присвоение значений в self.params
        """
        with open(name, "rb") as f:
            print("\nДанные прочитаны из pickle файла: {}\n".format(pickle.load(f)))

    def write(self, name):
        """
        Запись в формате pickle параметров self.params
        """
        with open(name, "wb") as f:
            pickle.dump(self.params, f)


ParamHandler.add_type("txt", TextParamHandler)
ParamHandler.add_type("xml", XmlParamHandler)
ParamHandler.add_type("json", JsonParamHandler)
ParamHandler.add_type("pickle", PickleParamHandler)

config = ParamHandler.get_instance('./params.json')
config.add_param('key1', 'val1')
config.add_param('key2', 'val2')
config.add_param('key3', 'val3')
config.write("params.json")
config.read("params.json")

config = ParamHandler.get_instance('./params.pickle')
config.add_param('key1', 'val1')
config.add_param('key2', 'val2')
config.add_param('key3', 'val3')
config.write("params.pickle")
config.read("params.pickle")



