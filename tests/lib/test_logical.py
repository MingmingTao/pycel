import pytest

from pycel.excelutil import (
    DIV0,
    ERROR_CODES,
    NA_ERROR,
    VALUE_ERROR,
)

from pycel.lib.logical import (
    _clean_logicals,
    iferror,
    x_and,
    x_if,
    x_not,
    x_or,
    x_xor,
)


@pytest.mark.parametrize(
    'test_value, result', (
        ((1, '3', 2.0, 3.1, ('x', True, None)),
         (1, 2, 3.1, True)),
        ((1, '3', 2.0, 3.1, ('x', VALUE_ERROR)),
         VALUE_ERROR),
        ((1, NA_ERROR, 2.0, 3.1, ('x', VALUE_ERROR)),
         NA_ERROR),
        (('1', ('x', 'y')),
         VALUE_ERROR),
        ((),
         VALUE_ERROR),
    )
)
def test_clean_logicals(test_value, result):
    assert _clean_logicals(*test_value) == result


@pytest.mark.parametrize(
    'result, test_value', (
        (False, (False,)),
        (True, (True,)),
        (True, (1, '3', 2.0, 3.1, ('x', True))),
        (True, (1, '3', 2.0, 3.1, ('x', True, None))),
        (False, (1, '3', 2.0, 3.1, ('x', False))),
        (VALUE_ERROR, (1, '3', 2.0, 3.1, ('x', VALUE_ERROR))),
        (NA_ERROR, (1, NA_ERROR, 2.0, 3.1, ('x', VALUE_ERROR))),
        (VALUE_ERROR, ('1', ('x', 'y'))),
        (VALUE_ERROR, (),),
        (NA_ERROR, (NA_ERROR, 1),),
    )
)
def test_x_and(result, test_value):
    assert x_and(*test_value) == result


def test_iferror():
    assert 'A' == iferror('A', 2)

    for error in ERROR_CODES:
        assert 2 == iferror(error, 2)


@pytest.mark.parametrize(
    'test_value, true_value, false_value, result', (
        ('xyzzy', 3, 2, VALUE_ERROR),
        ('0', 2, 1, VALUE_ERROR),
        (True, 2, 1, 2),
        (False, 2, 1, 1),
        ('True', 2, 1, 2),
        ('False', 2, 1, 1),
        (None, 2, 1, 1),
        (NA_ERROR, 0, 0, NA_ERROR),
        (DIV0, 0, 0, DIV0),
        (1, VALUE_ERROR, 1, VALUE_ERROR),
        (0, VALUE_ERROR, 1, 1),
        (0, 1, VALUE_ERROR, VALUE_ERROR),
        (1, 1, VALUE_ERROR, 1),
    )
)
def test_x_if(test_value, true_value, false_value, result):
    assert x_if(test_value, true_value, false_value) == result


@pytest.mark.parametrize(
    'result, test_value', (
        (False, True),
        (False, 1),
        (False, 2.1),
        (False, 'true'),
        (False, 'True'),
        (False, True),

        (True, False),
        (True, None),
        (True, 0),
        (True, 0.0),
        (True, 'false'),
        (True, 'faLSe'),

        (VALUE_ERROR, VALUE_ERROR),
        (NA_ERROR, NA_ERROR),
        (VALUE_ERROR, '3'),
        (VALUE_ERROR, ('1', ('x', 'y'))),
        (VALUE_ERROR, (),),
    )
)
def test_x_not(result, test_value):
    assert x_not(test_value) == result


@pytest.mark.parametrize(
    'result, test_value', (
        (False, (False,)),
        (True, (True,)),
        (True, (1, '3', 2.0, 3.1, ('x', True))),
        (True, (1, '3', 2.0, 3.1, ('x', False))),
        (False, (0, '3', 0.0, '3.1', ('x', False))),
        (VALUE_ERROR, (1, '3', 2.0, 3.1, ('x', VALUE_ERROR))),
        (NA_ERROR, (1, NA_ERROR, 2.0, 3.1, ('x', VALUE_ERROR))),
        (VALUE_ERROR, ('1', ('x', 'y'))),
        (VALUE_ERROR, (),),
    )
)
def test_x_or(result, test_value):
    assert x_or(*test_value) == result


@pytest.mark.parametrize(
    'result, test_value', (
        (False, (False,)),
        (True, (True,)),
        (False, (False, False)),
        (True, (False, True)),
        (True, (True, False)),
        (False, (False, False)),
        (False, (1, '3', 2.0, 3.1, ('x', True))),
        (True, (1, '3', 2.0, 3.1, ('x', False))),
        (False, (0, '3', 0.0, '3.1', ('x', False))),
        (VALUE_ERROR, (1, '3', 2.0, 3.1, ('x', VALUE_ERROR))),
        (NA_ERROR, (1, NA_ERROR, 2.0, 3.1, ('x', VALUE_ERROR))),
        (VALUE_ERROR, ('1', ('x', 'y'))),
        (VALUE_ERROR, (),),
    )
)
def test_x_xor(result, test_value):
    assert x_xor(*test_value) == result
