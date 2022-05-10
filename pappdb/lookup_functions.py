# string functions
def to_string(value):
    if value is None:
        return ''

    return str(value)


def contains(field_value, value):
    return to_string(value) in to_string(field_value)


def icontains(field_value, value):
    return to_string(value).lower() in to_string(field_value).lower()


def startswith(field_value, value):
    return to_string(field_value).startswith(to_string(value))


def istartswith(field_value, value):
    return to_string(field_value).lower().startswith(to_string(value).lower())


def endswith(field_value, value):
    return to_string(field_value).endswith(to_string(value))


def iendswith(field_value, value):
    return to_string(field_value).lower().endswith(to_string(value).lower())


# type functions
def is_none(field_value, should_be_none):
    result = field_value is None

    if not should_be_none:
        result = not result

    return result


def is_true(field_value, should_be_true):
    result = field_value is True

    if not should_be_true:
        result = not result

    return result


def is_false(field_value, should_be_false):
    result = field_value is False

    if not should_be_false:
        result = not result

    return result


def is_list(field_value, should_be_list):
    result = isinstance(field_value, list)

    if not should_be_list:
        result = not result

    return result


def is_dict(field_value, should_be_dict):
    result = isinstance(field_value, dict)

    if not should_be_dict:
        result = not result

    return result


SEPERATOR = '__'
DEFAULT_LOOKUP_FUNCTION_NAME = 'eq'

LOOKUP_FUNCTIONS = {
    # logic functions
    'eq': lambda field_value, value: field_value == value,
    'ne': lambda field_value, value: field_value != value,
    'lt': lambda field_value, value: field_value < value,
    'lte': lambda field_value, value: field_value <= value,
    'gt': lambda field_value, value: field_value > value,
    'gte': lambda field_value, value: field_value >= value,
    'in': lambda field_value, value: field_value in value,
    'passes': lambda field_value, test: test(field_value),

    # type functions
    'isnull': is_none,
    'isnone': is_none,
    'istrue': is_true,
    'isfalse': is_false,
    'islist': is_list,
    'isdict': is_dict,

    # string functions
    'contains': contains,
    'icontains': icontains,
    'startswith': startswith,
    'istartswith': istartswith,
    'endswith': endswith,
    'iendswith': iendswith,
}
