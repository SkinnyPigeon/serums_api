from components.users.add_or_remove_users import remove_user


def test_cannot_remove_unregistered_user():
    result = remove_user(2000, ['ustan'])
    assert result[1] == 500
