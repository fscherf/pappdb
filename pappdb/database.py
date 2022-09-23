from threading import RLock

from prettytable import PrettyTable

from pappdb.table import Table


class Database:
    def __init__(self):
        self._lock = RLock()
        self._tables = {}

    @property
    def lock(self):
        return self._lock

    def __repr__(self):
        with self.lock:
            pretty_table = PrettyTable(['Table Name', 'Columns', 'Rows'])

            for table_name in sorted(self.get_table_names()):
                table = self.get_table(table_name)

                pretty_table.add_row([
                    table_name,
                    len(table.get_column_names()),
                    len(table),
                ])

            return str(pretty_table)

    # tables ##################################################################
    def create_table(self, name):
        with self.lock:
            table = Table(
                database=self,
                name=name,
            )

            self._tables[name] = table

            return table

    def get_table_names(self):
        with self.lock:
            return list(self._tables.keys())

    def get_table(self, name):
        with self.lock:
            return self._tables[name]

    def get_or_create_table(self, name):
        with self.lock:
            if name not in self._tables:
                self.create_table(name)

            return self.get_table(name)

    def drop_tables(self):
        with self.lock:
            self._tables.clear()

    # datasets ################################################################
    def _load_dataset(self, dataset, clean):
        if clean:
            self.drop_tables()

        for table_name, rows in dataset.items():
            table = self.get_or_create_table(table_name)

            for row in rows:
                table.add_row(**row)

    # YAML
    def load_yaml_dataset(self, yaml_string, clean=True):
        import yaml

        with self.lock:
            self._load_dataset(
                dataset=yaml.safe_load(yaml_string),
                clean=clean,
            )

    def load_yaml_dataset_from_file(self, path, clean=True):
        with self.lock:
            with open(path, 'r') as stream:
                self.load_yaml_dataset(
                    yaml_string=stream.read(),
                    clean=clean,
                )
