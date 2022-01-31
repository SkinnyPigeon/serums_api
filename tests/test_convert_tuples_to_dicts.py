from components.utils.sqlalchemy_to_dict import convert_tuples_to_dict


def test_can_convert_tuples_to_dicts():
    row = (0, 'hello', 'me', 123.45)
    fields = ['count', 'greeting', 'who', 'number']
    result = convert_tuples_to_dict(row, fields)
    expected = {
        'count': 0,
        'greeting': 'hello',
        'who': 'me',
        'number': 123.45
    }
    assert result == expected
