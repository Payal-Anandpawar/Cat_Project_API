from datetime import datetime, timezone
from unittest import mock

import pytest

from myfirstcatapi import dto
from myfirstcatapi.domains import cat_domain
from tests import conftest

UTC = timezone.utc


@pytest.mark.parametrize(
    "new_cat, expected_cat",
    [
        (
            dto.UnsavedCat(
                name="Sammybridge Cat",
            ),
            dto.Cat(
                id=dto.CatID("000000000000000000000101"),
                name="Sammybridge Cat",
                ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            ),
        )
    ],
)
@mock.patch("myfirstcatapi.models.cat_model.create_cat")
@mock.patch("myfirstcatapi.libs.dates.get_utcnow")
@conftest.async_test
async def test_create_cat(
    mock_utcnow: mock.Mock,
    mock_cat_model_create_cat: mock.Mock,
    new_cat: dto.UnsavedCat,
    expected_cat: dto.Cat,
) -> None:
    mock_utcnow.return_value = datetime(2019, 1, 1, 23, 59, tzinfo=UTC)
    mock_cat_model_create_cat.return_value = expected_cat

    result = await cat_domain.create_cat(new_cat)

    assert result == expected_cat
    mock_cat_model_create_cat.assert_called_once_with(
        new_cat, now=datetime(2019, 1, 1, 23, 59, tzinfo=UTC)
    )


@pytest.mark.parametrize(
    "cat_filter",
    [
        dto.CatFilter(
            cat_id=dto.CatID("000000000000000000000101"),
            name="Sammybridge Cat",
        )
    ],
)
@mock.patch("myfirstcatapi.models.cat_model.find_one")
@conftest.async_test
async def test_find_one(mock_cat_model_find_one: mock.Mock, cat_filter: dto.CatFilter) -> None:
    await cat_domain.find_one(cat_filter)

    mock_cat_model_find_one.assert_called_once_with(cat_filter=cat_filter)


@pytest.mark.parametrize(
    "cat_filter, cat_sort_params, page",
    [
        (
            dto.CatFilter(
                cat_id=dto.CatID("000000000000000000000101"),
                name="Sammybridge Cat",
            ),
            [
                dto.CatSortPredicate(key=dto.CatSortKey.id, order=dto.SortOrder.asc),
                dto.CatSortPredicate(key=dto.CatSortKey.name, order=dto.SortOrder.desc),
            ],
            dto.Page(number=2, size=30),
        )
    ],
)
@mock.patch("myfirstcatapi.models.cat_model.find_many")
@conftest.async_test
async def test_find_many(
    mock_cat_model_find_many: mock.Mock,
    cat_filter: dto.CatFilter,
    cat_sort_params: dto.CatSortPredicates,
    page: dto.Page,
) -> None:
    await cat_domain.find_many(
        cat_filter=cat_filter,
        cat_sort_params=cat_sort_params,
        page=page,
    )

    mock_cat_model_find_many.assert_called_once_with(
        cat_filter=cat_filter,
        cat_sort_params=cat_sort_params,
        page=page,
    )


@pytest.mark.parametrize(
    "cat_id",
    ["000000000000000000000101"],
)
@mock.patch("myfirstcatapi.models.cat_model.delete_one")
@conftest.async_test
async def test_delete_one(mock_cat_model_delete_one: mock.Mock, cat_id: dto.CatID) -> None:
    await cat_domain.delete_one(cat_id)

    mock_cat_model_delete_one.assert_called_once_with(cat_id=cat_id)


@pytest.mark.parametrize(
    "cat_id, partial_update, expected_cat",
    [
        (
            dto.CatID("000000000000000000000101"),
            dto.PartialUpdateCat(url="http://placekitten.com/200/300"),
            dto.ResultCount(count=1),
        )
    ],
)
@mock.patch("myfirstcatapi.models.cat_model.update_cat_metadata")
@conftest.async_test
async def test_update_cat_metadata(
    mock_cat_model_update_cat_metadata: mock.Mock,
    cat_id: dto.CatID,
    partial_update: dto.PartialUpdateCat,
    expected_cat: dto.ResultCount,
) -> None:
    mock_cat_model_update_cat_metadata.return_value = expected_cat

    result = await cat_domain.update_cat_metadata(cat_id, partial_update)

    assert result == expected_cat
    mock_cat_model_update_cat_metadata.assert_called_once_with(
        cat_id=cat_id, partial_update=partial_update
    )
