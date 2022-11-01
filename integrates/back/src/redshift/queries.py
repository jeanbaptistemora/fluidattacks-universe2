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
