from enum import Enum

from pappdb.lookup import Lookup


class CONNECTOR(Enum):
    AND = 1
    OR = 2


class Q:
    def __init__(self, *qs, **raw_lookups):
        self._connector = CONNECTOR.AND
        self._negated = False
        self._qs = []
        self._lookups = []

        # check for valid call
        if not qs and not raw_lookups:
            raise ValueError('To few arguments')

        if qs and raw_lookups:
            raise ValueError('To many arguments')

        # add qs
        for q in qs:
            if not isinstance(q, Q):
                raise ValueError('Q object expected')

            self._qs.append(q)

        # lookups
        for key, value in raw_lookups.items():
            self._lookups.append(Lookup(key=key, value=value))

    def __repr__(self):
        repr_strings = []

        if self._qs:
            for q in self._qs:
                repr_strings.append(repr(q))

        elif self._lookups:
            for lookup in self._lookups:
                repr_strings.append(f'{lookup.key}={lookup.value!r}')

        connector_name = self._connector.name

        if self._negated:
            connector_name = f'NOT {connector_name}'

        return f"<{connector_name}({', '.join(repr_strings)})>"

    def __or__(self, other):
        q = Q(self, other)

        q._connector = CONNECTOR.OR

        return q

    def __and__(self, other):
        return Q(self, other)

    def __invert__(self):
        self._negated = not self._negated

        return self

    def check(self, row):
        result = None
        checks = self._qs or self._lookups

        for check in checks:
            result = check.check(row)

            if result:
                if self._connector == CONNECTOR.OR:
                    break

            else:
                if self._connector == CONNECTOR.AND:
                    break

        if self._negated:
            result = not result

        return result
