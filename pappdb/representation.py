from pprint import pformat


def column_to_string(column):
    from pappdb.table import Table
    from pappdb.row import Row

    if column is None:
        return ''

    if isinstance(column, (list, Table)):
        strings = []

        for item in column:
            strings.append(column_to_string(item))

        return f"[{', '.join(strings)}]"

    if isinstance(column, Row):
        return f"<Row(name={column.table.name})>"

    return pformat(column)
