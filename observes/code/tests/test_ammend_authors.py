import copy
import pytest
from code import ammend_authors


def test_get_mailmap_dict():
    mailmap_path = 'tests/mock_data/.mailmap'
    result = ammend_authors.get_mailmap_dict(mailmap_path)
    canon = ('Super Developer', 'sdev@canon.email.com')
    expected = {
        ('Super Developer', 'sdev95@flu-id.la'): canon,
        ('SDEV', 'sdev@canon.email.com'): canon,
        ('s.Dev-super V95', 'sdev95@alias.email.la'): canon,
        ('Super-Developer', 'sdev@other-domain'): canon,
    }
    assert expected == result


@pytest.mark.asyncio
async def test_get_items_to_change():
    canon = ('Super Developer', 'sdev@canon.email.com')
    alias = ('s.Dev-super V95', 'sdev95@alias.email.la')
    mailmap_dict = {
        alias: canon,
    }
    base_mock_item = {
        'hash': 'efwef4f42f23g',
        'namespace': 'the_namespace',
        'repository': 'super_repo',
        'author_email': canon[1],
        'author_name': canon[0],
        'committer_email': canon[1],
        'committer_name': canon[0],
    }
    mock_item_case_0 = ammend_authors.Item(**base_mock_item)

    mock_item_case_1 = copy.deepcopy(base_mock_item)
    mock_item_case_1['committer_email'] = alias[1]
    mock_item_case_1['committer_name'] = alias[0]
    mock_item_case_1 = ammend_authors.Item(**mock_item_case_1)

    mock_item_case_2 = copy.deepcopy(base_mock_item)
    mock_item_case_2['author_email'] = alias[1]
    mock_item_case_2['author_name'] = alias[0]
    mock_item_case_2 = ammend_authors.Item(**mock_item_case_2)

    mock_item_case_3 = copy.deepcopy(base_mock_item)
    mock_item_case_3['committer_email'] = alias[1]
    mock_item_case_3['committer_name'] = alias[0]
    mock_item_case_3['author_email'] = alias[1]
    mock_item_case_3['author_name'] = alias[0]
    mock_item_case_3 = ammend_authors.Item(**mock_item_case_3)

    mock_items = [
        mock_item_case_0, mock_item_case_1,
        mock_item_case_2, mock_item_case_3
    ]
    results = await ammend_authors.get_items_to_change(
        mock_items,
        mailmap_dict
    )

    for result in results:
        assert result.hash == mock_item_case_0.hash
        assert result.namespace == mock_item_case_0.namespace
        assert result.repository == mock_item_case_0.repository
        assert result.author_email == canon[1]
        assert result.author_name == canon[0]
        assert result.committer_email == canon[1]
        assert result.committer_name == canon[0]
