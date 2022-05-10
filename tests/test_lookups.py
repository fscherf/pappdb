import pytest


def test_Q_constructor():
    from pappdb import Q

    # to few arguments
    with pytest.raises(ValueError) as exc_info:
        Q()

    assert 'To few arguments' in str(exc_info.value)

    # to many arguments
    with pytest.raises(ValueError) as exc_info:
        Q(Q(a=1), b=2)

    assert 'To many arguments' in str(exc_info.value)

    # Q object expected
    with pytest.raises(ValueError) as exc_info:
        Q(1)

    assert 'Q object expected' in str(exc_info.value)


def test_basic_lookups():
    from pappdb import Q

    q = Q(a=1)

    assert q.check({'a': 1})
    assert not q.check({'a': 2})
    assert not q.check({'b': 1})
    assert not q.check({})

    # inverted
    q = ~Q(a=1)

    assert not q.check({'a': 1})
    assert q.check({'a': 2})
    assert q.check({'b': 1})
    assert q.check({})


def test_F_objects():
    from pappdb import Q, F

    q = Q(a=F('b'))

    assert q.check({'a': 1, 'b': 1})
    assert q.check({'a': 2, 'b': 2})
    assert not q.check({'a': 1, 'b': 2})
    assert not q.check({'a': 2, 'b': 1})


def test_or_connectors():
    from pappdb import Q

    q = Q(a=1) | Q(a=2)

    assert q.check({'a': 1})
    assert q.check({'a': 2})
    assert not q.check({'a': 3})


def test_and_connectors():
    from pappdb import Q

    # Qs connected with function args
    q = Q(a=1, b=1)

    assert q.check({'a': 1, 'b': 1})
    assert not q.check({'a': 1, 'b': 2})
    assert not q.check({'a': 2, 'b': 1})

    # Qs connected with operator
    q = Q(a=1) & Q(b=1)

    assert q.check({'a': 1, 'b': 1})
    assert not q.check({'a': 1, 'b': 2})
    assert not q.check({'a': 2, 'b': 1})
