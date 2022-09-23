from pprint import pformat

from prettytable import PrettyTable


class Row:
    def __init__(self, database, table, data=None):
        self._database = database
        self._table = table

        if data:
            self._data = {
                **data,
            }

        else:
            self._data = {}

    def __repr__(self):
        with self._database.lock:
            table = PrettyTable()
            row = []

            table.align = 'l'
            table.field_names = sorted(list(self._data.keys()))

            for column in table.field_names:
                row.append(pformat(self._data[column]))

            table.add_row(row)

            return str(table)

    def __len__(self):
        with self._database.lock:
            return len(self._data)

    def __getitem__(self, name):
        with self._database.lock:
            return self._data.get(name, None)

    def __setitem__(self, name, value):
        with self._database.lock:
            self._data[name] = value

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)

        except AttributeError:
            if not hasattr(self._data, name):
                raise

        attribute = self._data.__getattribute__(name)

        def shim(*args, **kwargs):
            with self._database.lock:
                return attribute(*args, **kwargs)

        if callable(attribute):
            return shim

        return attribute

    def __iter__(self):
        yield

    @property
    def database(self):
        return self._database

    @property
    def table(self):
        return self._table
