# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

SQL_INSERT_METADATA = """
    INSERT INTO {table} ({fields}) SELECT {values}
    WHERE NOT EXISTS (
        SELECT id
        FROM {table}
        WHERE id = %(id)s
    )
    """

SQL_INSERT_HISTORIC = """
    INSERT INTO {table_historic} ({fields}) SELECT {values}
    WHERE NOT EXISTS (
        SELECT id, modified_date
        FROM {table_historic}
        WHERE id = %(id)s and modified_date = %(modified_date)s
    ) AND EXISTS (
        SELECT id
        FROM {table_metadata}
        WHERE id = %(id)s
    )
    """
