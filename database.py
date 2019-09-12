import psycopg2
import psycopg2.extras
import config

class Connection:
    """
        Класс для коннекта к postgres (simple ORM)
    """

    def __init__(self):
        """  """
        self.connection = psycopg2.connect(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS,
                                           dbname=config.DB_NAME)
        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


class Query:

    def __init__(self, sql, connection, **kwargs):
        if kwargs:
            self.sql = sql.format(**kwargs)
        else:
            self.sql = sql

        self.connection = connection

    def set_params(self, **kwargs):
        self.sql = self.sql.format(**kwargs)

    def generate(self, **kwargs):
        if kwargs:
            self.sql = self.sql.format(**kwargs)
        return self.sql

    def execute(self, connection=None, **kwargs):
        if kwargs:
            self.sql = self.sql.format(**kwargs)

        connection = self.connection if isinstance(connection, type(None)) else connection
        connection.cursor.execute(self.sql)
        connection.connection.commit()

    def fetchall(self, connection=None, **kwargs):
        if kwargs:
            self.sql = self.sql.format(**kwargs)

        connection = self.connection if isinstance(connection, type(None)) else connection
        connection.cursor.execute(self.sql)
        return connection.cursor.fetchall()

    def fetchone(self, connection=None, **kwargs):
        if kwargs:
            self.sql = self.sql.format(**kwargs)
        connection = self.connection if isinstance(connection, type(None)) else connection
        cursor = connection.connection.cursor()
        cursor.execute(self.sql)
        return cursor.fetchone()



