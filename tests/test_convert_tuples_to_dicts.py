from components.utils.convert_to_dicts import tuples_as_dict


def test_can_convert_tuples_to_dicts():
    row = (0, 'hello', 'me', 123.45)
    fields = ['count', 'greeting', 'who', 'number']
    result = tuples_as_dict(row, fields)
    expected = {
        'count': 0,
        'greeting': 'hello',
        'who': 'me',
        'number': 123.45
    }
    assert result == expected
