from components.blockchain.lineage import create_record
import pytest


@pytest.mark.skip(reason="This is working so don't need to fill the db")
def test_can_create_record():
    result = create_record(117, 'TESTING', ['USTAN'])
    assert result[:6] == 'PROOF_'
