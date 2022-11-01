# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from string import (
    Template,
)

SQL_INSERT_METADATA = Template(
    """
    INSERT INTO ${table} (${fields}) SELECT ${values}
    WHERE NOT EXISTS (
        SELECT id
        FROM ${table}
        WHERE id = %(id)s
    )
    """
)

SQL_INSERT_METADATA_STR = """
    INSERT INTO {table} ({fields}) SELECT {values}
    WHERE NOT EXISTS (
        SELECT id
        FROM {table}
        WHERE id = %(id)s
    )
    """


SQL_INSERT_HISTORIC = Template(
    """
    INSERT INTO ${table} (${fields}) SELECT ${values}
    WHERE NOT EXISTS (
        SELECT id, modified_date
        FROM ${table}
        WHERE id = %(id)s and modified_date = %(modified_date)s
    )
    """
)
