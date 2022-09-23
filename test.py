from pappdb import Database, Q, F

import rlpython


database = Database()

manufacturer = database.create_table('Manufacturers')
owners = database.create_table('Owners')
cars = database.create_table('Cars')

# manufacturers
mercedes = manufacturer.add_row(
    name='Mercedes',
    country='Germany',
)

bmw = manufacturer.add_row(
    name='BMW',
    country='Germany',
)

volvo = manufacturer.add_row(
    name='Volvo',
    country='Sweden',
)

# owners
alice = owners.add_row(
    name='Alice',
)

bob = owners.add_row(
    name='Bob',
)

# cars
xc_90 = cars.add_row(
    name='XC 90',
    manufacturer=volvo,
    owner=alice,
)

a_class = cars.add_row(
    name='A Class',
    manufacturer=mercedes,
    owner=bob,
)

c_class = cars.add_row(
    name='C Class',
    manufacturer=mercedes,
    owner=[bob, alice],
)

c_class = cars.add_row(
    name='S Class',
    manufacturer=mercedes,
)


rlpython.embed()
