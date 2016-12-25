import os
import psycopg2
from urllib.parse import urlparse


class Connection:
    def __init__(self):
        self.connection = self._get_connection()

    def _get_connection(self):
        if 'DATABASE_URL' not in os.environ:
            raise RuntimeError('Missing DATABASE_URL environment variable')
        params = self._get_url_params(os.environ['DATABASE_URL'])
        return psycopg2.connect(**params)

    def _get_url_params(self, url):
        url = urlparse(url)
        return {
            'database': url.path[1:],
            'user': url.username,
            'password': url.password,
            'host': url.hostname,
            'port': url.port,
        }

    def cursor(self):
        cursor = self.connection.cursor()

        class Cursor():
            def __enter__(self):
                self.cursor = cursor
                return self.cursor

            def __exit__(self, a, b, c):
                self.cursor.close()

        return Cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
