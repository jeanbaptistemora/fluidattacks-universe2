from custom_exceptions import (
    InvalidMobileNumber,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
)
import pytest
from stakeholders import (
    validations,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ("new_phone",),
    (
        (
            StakeholderPhone(
                national_number="12345",
                calling_country_code="1234",
                country_code="",
            ),
        ),
        (
            StakeholderPhone(
                national_number="123456789012345",
                calling_country_code="1",
                country_code="",
            ),
        ),
    ),
)
def test_validate_phone(
    new_phone: StakeholderPhone,
) -> None:
    phone = StakeholderPhone(
        national_number="12345",
        calling_country_code="1",
        country_code="",
    )
    validations.validate_phone(phone)
    with pytest.raises(InvalidMobileNumber):
        validations.validate_phone(new_phone)
