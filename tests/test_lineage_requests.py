from components.blockchain.lineage import create_record, \
                                          hash_columns
import pytest


# @pytest.mark.skip(reason="This is working so don't need to fill the db")
def test_can_create_record():
    result = create_record(117, 'TESTING', ['ustan'])
    assert result[:6] == 'PROOF_'


def test_can_hash_columns():
    columns = ['c', 'b', 'a']
    result = hash_columns(columns)
    assert result == 'ba7816bf8f01cfea414140de5dae2223'\
                     'b00361a396177a9cb410ff61f20015ad'
    changed_order_columns = sorted(columns)
    assert columns != changed_order_columns
    changed_order_result = hash_columns(changed_order_columns)
    assert result == changed_order_result
