from components.users.add_or_remove_users import remove_user, \
                                                 add_user


def test_cannot_remove_unregistered_user():
    result = remove_user(2000, ['ustan'])
    assert result[0]['ustan'] == {
        "message": "User not found in USTAN"
    }


def test_can_add_new_user():
    remove_user(9876, ['ustan'])
    result = add_user(9876, 9876, 'ustan')
    assert result[1] == 200


def cannot_insert_user_with_duplicate_serums_id():
    add_user(4242, 1234, 'ustan')
    result = add_user(4242, 1234, 'ustan')
    assert result[1] == 500
