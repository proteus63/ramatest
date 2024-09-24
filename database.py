from json import dumps, loads
from os import makedirs
from os.path import join, exists

from peewee import CharField, Model, SmallIntegerField, SQL, SqliteDatabase
from playhouse.sqlite_ext import DateTimeField

from request import Request

class JSONField(CharField):
    def db_value(self, value):
        if isinstance(value, str):
            return value
        else:
            return dumps(value)

    def python_value(self, value):
        return loads(value)


class ExternalDatabase(object):
    profile_path = "stremio_profile_path"  # Definisci il path del profilo per Stremio
    connection = SqliteDatabase(join(profile_path, 'dramacool.db'))

    @classmethod
    def close(cls):
        cls.connection.close()

    @classmethod
    def connect(cls):
        if not exists(cls.profile_path):
            makedirs(cls.profile_path)
        cls.connection.connect(True)

    @classmethod
    def create(cls):
        cls.connection.create_tables([RecentDrama, RecentFilter])
        cls.connection.commit()


class InternalDatabase(object):
    addon_path = "stremio_addon_path"  # Definisci il path per i dati interni dell'addon
    connection = SqliteDatabase(join(addon_path, 'dramacool.db'))

    @classmethod
    def close(cls):
        if cls.connection:
            cls.connection.close()

    @classmethod
    def connect(cls):
        cls.connection.connect(True)

    @classmethod
    def create(cls):
        cls.connection.create_tables([Drama])

        paths = {drama.path for drama in Drama.select().where((Drama.status == 33710) & Drama.category.is_null(False))}
        categories = ['/category/korean-movies', '/category/japanese-movies', '/category/taiwanese-movies',
                      '/category/hong-kong-movies', '/category/chinese-movies', '/category/american-movies',
                      '/category/other-asia-movies', '/category/thailand-movies', '/category/indian-movies',
                      '/category/korean-drama', '/category/japanese-drama', '/category/taiwanese-drama',
                      '/category/hong-kong-drama', '/category/chinese-drama',
                      '/category/american-drama', '/category/other-asia-drama', '/category/thailand-drama',
                      '/category/indian-drama', '/kshow']

        for category in categories:
            for path in Request.drama_list(category):
                if path not in paths:
                    Drama.create(**Request.drama_detail(path, category))

        cls.connection.commit()


class ExternalModel(Model):
    class Meta:
        database = ExternalDatabase.connection


class InternalModel(Model):
    class Meta:
        database = InternalDatabase.connection


class Drama(InternalModel):
    path = CharField(primary_key=True, constraints=[SQL('ON CONFLICT REPLACE')])
    category = CharField(null=True)
    poster = CharField()
    title = CharField()
    plot = CharField()
    country = SmallIntegerField()
    status = SmallIntegerField()
    genre = JSONField()
    year = SmallIntegerField()

    def __init__(self, *args, **kwargs):
        super(Drama, self).__init__(*args, **kwargs)
        self.title = kwargs['title']
        self.poster = kwargs.get('poster', '')
        self.plot = kwargs.get('plot', '')


class RecentDrama(ExternalModel):
    path = CharField(primary_key=True, constraints=[SQL('ON CONFLICT REPLACE')])
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


class RecentFilter(ExternalModel):
    path = CharField(primary_key=True, constraints=[SQL('ON CONFLICT REPLACE')])
    title = CharField()
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


if __name__ == '__main__':
    try:
        InternalDatabase.connect()
        InternalDatabase.create()
    finally:
        InternalDatabase.close()
