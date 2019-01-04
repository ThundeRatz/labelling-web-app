import os
import psycopg2
from urllib.parse import urlparse

from flask import current_app


class Connection:
    def __init__(self):
        self.connection = self._get_connection()

    def _get_connection(self):
        try:
            params = current_app.config["DATABASE"]
        except KeyError:
            raise RuntimeError("Missing DATABASE config variable")
        return psycopg2.connect(**params)

    def cursor(self):
        cursor = self.connection.cursor()

        class Cursor:
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
