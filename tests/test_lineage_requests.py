from components.blockchain.lineage import create_record
import pytest


@pytest.mark.skip(
    reason="Blockchain lineage is not accepting list of hospital ids"
)
def test_can_create_record():
    result = create_record(117, 'TESTING', ['ustan'])
    assert type(result) == str
    assert result[:5] == 'RULE_'
