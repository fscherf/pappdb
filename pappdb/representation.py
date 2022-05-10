from pprint import pformat
from copy import deepcopy
from io import StringIO


def write_attribute_table(row, buffer=None):
    buffer = buffer or StringIO()
    row = deepcopy(row)  # FIXME

    # keys
    keys = sorted(row.keys())
    legend_width = max([len(key) for key in keys]) + 1

    # values
    for key_index, key in enumerate(keys):
        row[key] = pformat(row[key]).splitlines()

        if key_index > 0 and len(row[key]) > 1:
            buffer.write('\n')

        for line_index, line in enumerate(row[key]):
            if line_index == 0:
                buffer.write(f'{key.rjust(legend_width)}: {line}\n')

            else:
                buffer.write(f'{legend_width * " "}  {line}\n')

        if key_index < len(keys) and len(row[key]) > 1:
            buffer.write('\n')

    return buffer


def write_table(rows, buffer=None):
    buffer = buffer or StringIO()
    rows = deepcopy(rows)  # FIXME

    # find column widths
    column_widths = [[] for i in range(len(rows[0]))]

    for row_index, row in enumerate(rows):
        for column_index, column in enumerate(row):
            if column is None:
                lines = ['']

            elif row_index == 0:
                lines = str(column).strip().splitlines()

            else:
                lines = pformat(column).splitlines()

            rows[row_index][column_index] = lines

            column_widths[column_index].append(
                max([0] + [len(line) for line in lines])
            )

    for index, column_width in enumerate(column_widths):
        column_widths[index] = max(column_widths[index])

    # write table out
    def get_row_len(row):
        return max([len(i) for i in row])

    def write_divider():
        for column_width in column_widths:
            buffer.write('+')
            buffer.write('-' * (column_width + 2))

        buffer.write('+\n')

    def write_empty_row():
        for column_width in column_widths:
            buffer.write('|')
            buffer.write(' ' * (column_width + 2))

        buffer.write('|\n')

    def write_row(row):
        lines = get_row_len(row)
        row_index = rows.index(row)

        if lines > 1 and row_index > 1:
            write_empty_row()

        for line_index in range(lines):
            buffer.write('| ')

            for column_index, column in enumerate(row):
                if line_index < len(column):
                    line = column[line_index]

                else:
                    line = ''

                buffer.write(line.ljust(column_widths[column_index]))
                buffer.write(' | ')

            buffer.write('\n')

        if(lines > 1 and
           row_index < len(rows) - 1 and
           get_row_len(rows[row_index+1]) < 2):

            write_empty_row()

    write_divider()
    write_row(rows[0])
    write_divider()

    for row in rows[1:]:
        write_row(row)

    write_divider()

    return buffer
