from pappdb import Database, Q

db = Database()
table = db.get_or_create_table('numbers')

for number in range(100):
    row = {
        'name': f'Number {number}',
        'number': number,
    }

    if number == 0:
        row['foo'] = 'bar'

    table.add_row(row)


import rlpython
rlpython.embed()
