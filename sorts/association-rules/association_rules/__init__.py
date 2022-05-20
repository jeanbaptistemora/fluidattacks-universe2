from mlxtend.frequent_patterns import (  # type: ignore[import]
    apriori,
    association_rules,
)
from mlxtend.preprocessing import (  # type: ignore[import]
    TransactionEncoder,
)
import os
import pandas as pd  # type: ignore[import]
from pandas.core.frame import (  # type: ignore[import]
    DataFrame,
)
from pathlib import (
    Path,
)
import psycopg2  # type: ignore[import]
from psycopg2 import (
    extras,
)
from typing import (
    Any,
    List,
    Tuple,
)


def connection() -> Tuple[Any, Any]:
    con = psycopg2.connect(
        dbname=os.environ["REDSHIFT_DATABASE"],
        user=os.environ["REDSHIFT_USER"],
        password=os.environ["REDSHIFT_PASSWORD"],
        host=os.environ["REDSHIFT_HOST"],
        port=os.environ["REDSHIFT_PORT"],
    )
    cur = con.cursor()
    return (con, cur)


def execute_query(cur: Any, query: str) -> List[Tuple[str, ...]]:
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return list(data)


def generate_dataset(data: List[Tuple[str, ...]]) -> List[List[str]]:
    data_dict = {}
    for reg in data:
        index = reg[1] + "-" + reg[5]
        if index not in data_dict:
            data_dict[index] = {reg[4]}
        else:
            data_dict[index].add(reg[4])
    return [list(x) for x in data_dict.values()]


def generate_sparse_matrix(dataset: List[List[str]]) -> DataFrame:
    tr_enc = TransactionEncoder()
    sparse_dataset = tr_enc.fit(dataset).transform(dataset, sparse=True)
    sparse_df = pd.DataFrame.sparse.from_spmatrix(
        sparse_dataset, columns=tr_enc.columns_
    )
    return sparse_df


def get_itemsets(
    sparse_df: DataFrame,
    min_support: float = 0.00004,
    use_colnames: bool = True,
    verbose: int = 1,
) -> DataFrame:
    return apriori(
        sparse_df,
        min_support=min_support,
        use_colnames=use_colnames,
        verbose=verbose,
    )


def get_rules(
    frequent_itemsets: DataFrame,
    metric: str = "confidence",
    min_threshold: float = 0.02,
) -> DataFrame:
    return association_rules(
        frequent_itemsets, metric=metric, min_threshold=min_threshold
    )


def prepare_to_upload(rules: DataFrame) -> DataFrame:
    to_upload = rules.copy()
    to_upload["antecedents"] = (
        to_upload["antecedents"]
        .apply(lambda x: ", ".join(list(x)))
        .astype("unicode")
    )
    to_upload["consequents"] = (
        to_upload["consequents"]
        .apply(lambda x: ", ".join(list(x)))
        .astype("unicode")
    )
    mapper = {
        "antecedent support": "antecedent_support",
        "consequent support": "consequent_support",
    }
    to_upload.rename(mapper, axis=1, inplace=True)
    return to_upload


def prepare_table(conn: Any, schema: str, table: str) -> None:
    """
    Checks if the table exists, if it does not exist a new table
    is generated, if the table does exist its content is dropped
    so it can be replaced with new info
    """
    cur = conn.cursor()
    check_query = f"""SELECT EXISTS (
    SELECT * FROM pg_catalog.pg_class c
    JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = {schema}
    AND c.relname = {table}
    );"""
    response = cur.execute(check_query)
    cur.close()
    table_full = schema + "." + table
    if response:
        cur = conn.cursor()
        drop_query = f"DROP FROM {table_full}"
        cur.execute(drop_query)
        conn.commit()
        cur.close()
    if not response:
        cur = conn.cursor()
        create_query = f"""
        CREATE TABLE {table_full} (
        antecedents VARCHAR(3000),
        consequents VARCHAR(3000),
        antecedent_support FLOAT,
        consequent_support FLOAT,
        support FLOAT,
        confidence FLOAT,
        lift FLOAT,
        leverage FLOAT,
        conviction FLOAT"""
        cur.execute(create_query)
        conn.commit()
        cur.close()


def execute_values(conn: Any, dataframe: DataFrame, table: str) -> int:
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in dataframe.to_numpy()]
    # Comma-separated dataframe columns
    cols = ",".join(list(dataframe.columns))
    # SQL query to execute
    query = f"INSERT INTO {table}({cols}) VALUES %s"
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        cursor.close()
        return 1
    print("execute_values() done")
    cursor.close()
    return 0


def main() -> None:
    path = str(Path(__file__).parent / Path("extract_features.sql"))
    with open(path, encoding="UTF-8") as file:
        query = file.read()

    con, cur = connection()
    data = execute_query(cur, query)
    dataset = generate_dataset(data)
    sparse_m = generate_sparse_matrix(dataset)
    itemsets = get_itemsets(sparse_m)
    rules = get_rules(itemsets)
    to_upload = prepare_to_upload(rules)
    prepare_table(con, "sorts", "association_rules")
    execute_values(con, to_upload, "sorts.association_rules")
    con.close()
