from pappdb import Database, Q, F

import rlpython

dataset_path = '/home/fscherf/devel/pappdb/examples/cars.yml'


db = Database()
db.load_yaml_dataset_from_file(dataset_path)

table = db.get_table('car')


rlpython.embed()
