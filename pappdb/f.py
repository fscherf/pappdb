from pappdb.lookup_functions import SEPERATOR


class F:
    def __init__(self, field_name):
        self.field_name = field_name
        self.field_path = self.field_name.split(SEPERATOR)

    def __repr__(self):
        return f'<F({self.field_name})>'
