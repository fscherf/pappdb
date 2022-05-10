from pappdb.representation import write_attribute_table


class Row:
    def __init__(self, database, data=None):
        self._database = database

        if data:
            self._data = {
                **data,
            }

        else:
            self._data = {}

    def __repr__(self):
        with self._database.lock:
            buffer = write_attribute_table(self._data)

            buffer.seek(0)

            return buffer.read()

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
