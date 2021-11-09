from code_etl.amend_authors import (
    Amend,
    Item,
)
import copy
import pytest


def test_get_mailmap_dict() -> None:
    mailmap_path = "tests/mock_data/.mailmap"
    amend = Amend("foo", "group1", mailmap_path)
    result = amend.get_mailmap_dict()
    canon = ("Super Developer", "sdev@canon.email.com")
    expected = {
        ("Super Developer", "sdev95@flu-id.la"): canon,
        ("SDEV", "sdev@canon.email.com"): canon,
        ("s.Dev-super V95", "sdev95@alias.email.la"): canon,
        ("Suññér-Dèvèlopèr", "çsdev@other-domain"): canon,
        ("s.Dèv-supér V95ç", "sdév95@açias.email.ça"): canon,
    }
    assert expected == result


@pytest.mark.asyncio
async def test_get_items_to_change() -> None:
    # pylint: disable=too-many-locals
    mailmap_path = "tests/mock_data/.mailmap"
    amend = Amend("foo", "group1", mailmap_path)
    canon = ("Super Developer", "sdev@canon.email.com")
    alias = ("s.Dèv-supér V95ç", "sdév95@açias.email.ça")
    mailmap_dict = {
        alias: canon,
    }
    base_mock_item = {
        "hash": "efwef4f42f23g",
        "namespace": "the_namespace",
        "repository": "super_repo",
        "author_email": canon[1],
        "author_name": canon[0],
        "committer_email": canon[1],
        "committer_name": canon[0],
    }
    mock_item_case_0 = Item(**base_mock_item)

    mock_item_case_1_dct = copy.deepcopy(base_mock_item)
    mock_item_case_1_dct["committer_email"] = alias[1]
    mock_item_case_1_dct["committer_name"] = alias[0]
    mock_item_case_1 = Item(**mock_item_case_1_dct)

    mock_item_case_2_dct = copy.deepcopy(base_mock_item)
    mock_item_case_2_dct["author_email"] = alias[1]
    mock_item_case_2_dct["author_name"] = alias[0]
    mock_item_case_2 = Item(**mock_item_case_2_dct)

    mock_item_case_3_dct = copy.deepcopy(base_mock_item)
    mock_item_case_3_dct["committer_email"] = alias[1]
    mock_item_case_3_dct["committer_name"] = alias[0]
    mock_item_case_3_dct["author_email"] = alias[1]
    mock_item_case_3_dct["author_name"] = alias[0]
    mock_item_case_3 = Item(**mock_item_case_3_dct)

    mock_items = [
        mock_item_case_0,
        mock_item_case_1,
        mock_item_case_2,
        mock_item_case_3,
    ]
    results = await amend.get_items_to_change(mock_items, mailmap_dict)

    for result in results:
        assert result.hash == mock_item_case_0.hash
        assert result.namespace == mock_item_case_0.namespace
        assert result.repository == mock_item_case_0.repository
        assert result.author_email == canon[1]
        assert result.author_name == canon[0]
        assert result.committer_email == canon[1]
        assert result.committer_name == canon[0]
