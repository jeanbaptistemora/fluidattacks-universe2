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
