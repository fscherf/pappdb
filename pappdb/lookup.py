from pappdb.lookup_functions import (
    DEFAULT_LOOKUP_FUNCTION_NAME,
    LOOKUP_FUNCTIONS,
    SEPERATOR,
)

from pappdb.f import F


class Lookup:
    def __init__(self, key, value):
        self.key = key
        self.value = value

        self.lookup_function_name = DEFAULT_LOOKUP_FUNCTION_NAME
        self.field_path = key.split(SEPERATOR)

        if self.field_path[-1] in LOOKUP_FUNCTIONS:
            self.lookup_function_name = self.field_path.pop()

        self.lookup_function = LOOKUP_FUNCTIONS[self.lookup_function_name]

    def _get_field_value(self, row, field_path=None):
        field_path = field_path or self.field_path
        field_value = None

        for field_name in field_path:
            try:
                row = row[field_name]
                field_value = row

            except Exception:
                break

        return field_value

    def check(self, row):
        field_value = self._get_field_value(row)
        value = self.value

        if isinstance(self.value, F):
            value = self._get_field_value(
                row=row,
                field_path=value.field_path,
            )

        try:
            return self.lookup_function(field_value, value)

        except TypeError:
            return False
