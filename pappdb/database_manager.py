from string import ascii_lowercase, digits
from threading import RLock
from random import choice

from pappdb.database import Database

RANDOM_NAME_LETTERS = ascii_lowercase + digits
RANDOM_NAME_LENGTH = 8
RANDOM_NAME_TRIES = 8


class DatabaseManager:
    def __init__(self):
        self._lock = RLock()
        self._databases = {}

        self.create_database(name='default')

    @property
    def lock(self):
        return self._lock

    def _generate_random_name(self):
        return ''.join([
            choice(RANDOM_NAME_LETTERS) for _ in range(RANDOM_NAME_LENGTH)
        ])

    def get_database_names(self):
        with self.lock:
            return list(self._databases.keys())

    def get_database(self, name='default'):
        with self.lock:
            if name not in self._databases:
                raise RuntimeError(
                    f"Database with name '{name}' does not exist",
                )

            return self._databases[name]

    def create_database(self, name='default'):
        with self.lock:
            if name in self._databases:
                raise RuntimeError(
                    f"Database with name '{name}' already exists",
                )

            self._databases[name] = Database()

    def delete_database(self, name):
        with self.lock:
            if name not in self._databases:
                raise RuntimeError(
                    f"Database with name '{name}' does not exist",
                )

            del self._databases[name]

    def clear_databases(self):
        with self.lock:
            self._databases.clear()

    def get_or_create_database(self, name):
        with self.lock:
            if name not in self._databases:
                self.create_database(name)

            return self._databases[name]

    def create_random_database(self):
        with self.lock:
            for _ in range(RANDOM_NAME_TRIES):
                database_name = self._generate_random_name()

                if database_name in self._databases:
                    continue

                self.create_database(name=database_name)

                return database_name

            raise RuntimeError('Cannot generate random name')
