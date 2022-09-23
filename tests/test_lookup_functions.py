# logic lookup functions ######################################################
def test_eq():
    from pappdb import Q

    # implicit 'eq'
    q = Q(a=1)

    assert q.check({'a': 1})
    assert not q.check({'a': 2})

    # explicit 'eq'
    q = Q(a__eq=1)

    assert q.check({'a': 1})
    assert not q.check({'a': 2})


def test_ne():
    from pappdb import Q

    q = Q(a__ne=1)

    assert q.check({'a': 2})
    assert not q.check({'a': 1})


def test_lt():
    from pappdb import Q

    q = Q(a__lt=1)

    assert q.check({'a': 0})
    assert not q.check({'a': 1})


def test_lte():
    from pappdb import Q

    q = Q(a__lte=1)

    assert q.check({'a': 0})
    assert q.check({'a': 1})
    assert not q.check({'a': 2})


def test_gt():
    from pappdb import Q

    q = Q(a__gt=1)

    assert q.check({'a': 2})
    assert not q.check({'a': 1})


def test_in():
    from pappdb import Q

    q = Q(a__in=[1, 2])

    assert q.check({'a': 1})
    assert q.check({'a': 2})
    assert not q.check({'a': 3})


def test_passes():
    from pappdb import Q

    q = Q(a__passes=lambda field_value: field_value == 1)

    assert q.check({'a': 1})
    assert not q.check({'a': 2})


# string lookup functions #####################################################
def test_contains():
    from pappdb import Q

    q = Q(a__contains='o')

    assert q.check({'a': 'foo'})
    assert q.check({'a': ['f', 'o', 'o']})
    assert not q.check({'a': 'bar'})
    assert not q.check({'a': ['b', 'a', 'r']})


def test_icontains():
    from pappdb import Q

    q = Q(a__icontains='o')

    # lowercase
    assert q.check({'a': 'foo'})
    assert q.check({'a': ['f', 'o', 'o']})
    assert not q.check({'a': 'bar'})
    assert not q.check({'a': ['b', 'a', 'r']})

    # uppercase
    assert q.check({'a': 'FOO'})
    assert q.check({'a': ['F', 'O', 'O']})
    assert not q.check({'a': 'BAR'})
    assert not q.check({'a': ['B', 'A', 'R']})


def test_startswith():
    from pappdb import Q

    q = Q(a__startswith='foo')

    assert q.check({'a': 'foobar'})
    assert q.check({'a': 'foo'})
    assert not q.check({'a': 'fo'})
    assert not q.check({'a': 'bar'})


def test_istartswith():
    from pappdb import Q

    q = Q(a__istartswith='foo')

    # lowercase
    assert q.check({'a': 'foobar'})
    assert q.check({'a': 'foo'})
    assert not q.check({'a': 'fo'})
    assert not q.check({'a': 'bar'})

    # uppercase
    assert q.check({'a': 'FOOBAR'})
    assert q.check({'a': 'FOO'})
    assert not q.check({'a': 'FO'})
    assert not q.check({'a': 'BAR'})


def test_endswith():
    from pappdb import Q

    q = Q(a__endswith='foo')

    assert q.check({'a': 'barfoo'})
    assert q.check({'a': 'foo'})
    assert not q.check({'a': 'fo'})
    assert not q.check({'a': 'bar'})


def test_iendswith():
    from pappdb import Q

    q = Q(a__iendswith='foo')

    # lowercase
    assert q.check({'a': 'barfoo'})
    assert q.check({'a': 'foo'})
    assert not q.check({'a': 'fo'})
    assert not q.check({'a': 'bar'})

    # uppercase
    assert q.check({'a': 'BARFOO'})
    assert q.check({'a': 'FOO'})
    assert not q.check({'a': 'FO'})
    assert not q.check({'a': 'BAR'})


# type lookup functions #######################################################
def test_isnone():
    from pappdb import Q

    q = Q(a__isnone=True)

    assert q.check({'a': None})
    assert q.check({})
    assert not q.check({'a': 1})
    assert not q.check({'a': []})

    q = Q(a__isnone=False)

    assert not q.check({'a': None})
    assert not q.check({})
    assert q.check({'a': 1})
    assert q.check({'a': []})


def test_isnull():
    from pappdb import Q

    q = Q(a__isnull=True)

    assert q.check({'a': None})
    assert not q.check({'a': 1})
    assert not q.check({'a': []})

    q = Q(a__isnull=False)

    assert not q.check({'a': None})
    assert q.check({'a': 1})
    assert q.check({'a': []})


def test_istrue():
    from pappdb import Q

    q = Q(a__istrue=True)

    assert q.check({'a': True})
    assert not q.check({'a': 1})
    assert not q.check({'a': [1]})

    q = Q(a__istrue=False)

    assert not q.check({'a': True})
    assert q.check({'a': 1})
    assert q.check({'a': [1]})


def test_isfalse():
    from pappdb import Q

    q = Q(a__isfalse=True)

    assert q.check({'a': False})
    assert not q.check({'a': 1})
    assert not q.check({'a': [1]})

    q = Q(a__isfalse=False)

    assert not q.check({'a': False})
    assert q.check({'a': 1})
    assert q.check({'a': [1]})


def test_islist():
    from pappdb import Q

    q = Q(a__islist=True)

    assert q.check({'a': []})
    assert q.check({'a': [1]})
    assert not q.check({'a': 1})

    q = Q(a__islist=False)

    assert not q.check({'a': []})
    assert not q.check({'a': [1]})
    assert q.check({'a': 1})


def test_isdict():
    from pappdb import Q

    q = Q(a__isdict=True)

    assert q.check({'a': {}})
    assert q.check({'a': {'a': 'a'}})
    assert not q.check({'a': 1})

    q = Q(a__isdict=False)

    assert not q.check({'a': {}})
    assert not q.check({'a': {'a': 'a'}})
    assert q.check({'a': 1})
