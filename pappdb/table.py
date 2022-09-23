from pprint import pformat

from prettytable import PrettyTable

from pappdb.representation import column_to_string
from pappdb.row import Row
from pappdb.q import Q

DEFAULT_PAGE_LENGTH = 30


class Table:
    def __init__(self, database, name, rows=None):
        self._database = database
        self._name = name

        self._columns = {}

        if rows:
            self._rows = [*rows]

            self._find_columns()

        else:
            self._rows = []

    def __iter__(self):
        with self._database.lock:
            return iter(self._rows)

    def __len__(self):
        with self._database.lock:
            return len(self._rows)

    def __getitem__(self, key):
        with self._database.lock:
            if isinstance(key, slice):
                return Table(
                    database=self._database,
                    rows=self._rows[key],
                )

            return self._rows[key]

    # string representation ###################################################
    def __repr__(self):
        if not self._rows:
            return f'<Table(name={self._name}, rows=[])>'

        with self._database.lock:

            # pagination
            if len(self) > DEFAULT_PAGE_LENGTH:
                pages = self.get_pagination_pages()
                rows = len(self)
                table = repr(self.get_pagination_page(0))

                return f'{table}\n{rows} rows (Page 1 of {pages})\n'

            # string representation
            column_names = self.get_column_names()
            pretty_table = PrettyTable(column_names)

            pretty_table.align = 'l'

            for row in self._rows:
                pretty_table.add_row([
                    column_to_string(row[name])
                    for name in column_names
                ])

            return str(pretty_table)

    @property
    def name(self):
        return self._name

    # columns #################################################################
    def _add_column(self, name):
        if name not in self._columns:
            self._columns[name] = 0

        self._columns[name] += 1

    def _remove_column(self, name):
        if name not in self._columns:
            return

        self._columns[name] -= 1

        if self._columns[name] == 0:
            del self._columns[name]

    def _remove_columns(self, row):
        for column_name in row.keys():
            self._remove_column(column_name)

    def _find_columns(self):
        self._columns.clear()

        for row in self._rows:
            for column in row.keys():
                self._add_column(column)

    def get_column_names(self):
        with self._database.lock:
            return sorted(list(self._columns.keys()))

    # rows ####################################################################
    def add_row(self, row=None, **row_data):
        with self._database.lock:
            if row:
                if not isinstance(row, Row):
                    row = Row(
                        database=self._database,
                        data=row,
                    )

                self._rows.append(row)

                for column in row.keys():
                    self._add_column(column)

                return row

            row = Row(
                database=self._database,
                table=self,
            )

            for name, value in row_data.items():
                self._add_column(name)
                row[name] = value

            self._rows.append(row)

            return row

    def delete_rows(self, *rows):
        with self._database.lock:
            for row in rows:
                self._rows.remove(row)
                self._remove_columns(row)

    # pagination ##############################################################
    def get_pagination_pages(self, page_length=DEFAULT_PAGE_LENGTH):
        with self._database.lock:
            rows = len(self._rows)
            pages = (rows - (rows % page_length)) // page_length

            if rows % page_length > 0:
                pages += 1

            return pages

    def get_pagination_page(self, page_index, page_length=DEFAULT_PAGE_LENGTH):
        with self._database.lock:
            start_index = page_index * page_length
            end_index = start_index + page_length

            return Table(
                database=self._database,
                name=self._name,
                rows=self._rows[start_index:end_index],
            )

    # filtering ###############################################################
    def all(self):
        return self

    def _filter(self, negated, *args, **kwargs):
        if len(args) == 1:
            q = Q(args[0])

        elif kwargs:
            q = Q(**kwargs)

        else:
            raise ValueError()

        if negated:
            q = ~q

        with self._database.lock:
            table = Table(
                database=self._database,
                name=self._name,
            )

            for row in self._rows:
                if not q.check(row):
                    continue

                table.add_row(row)

            return table

    def filter(self, *args, **kwargs):
        return self._filter(False, *args, **kwargs)

    def exclude(self, *args, **kwargs):
        return self._filter(True, *args, **kwargs)

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    # sorting #################################################################
    def reverse(self):
        with self._database.lock:
            return Table(
                database=self._database,
                name=self._name,
                rows=self._rows[::-1],
            )

    def order_by(self, column):
        reverse = False

        if column.startswith('-'):
            reverse = True
            column = column[1:]

        with self._database.lock:
            rows = sorted(
                self._rows,
                key=lambda row: row[column],
                reverse=reverse,
            )

            return Table(
                database=self._database,
                name=self._name,
                rows=rows,
            )
