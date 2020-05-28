# -*- coding: utf-8 -*-
"""This module provide a connection with neo4j."""

# standard imports
from typing import Optional, Dict, Iterator, Any, NamedTuple
from contextlib import contextmanager

# 3rd party imports
from neo4j import GraphDatabase, Session
from neo4j.api import DEFAULT_DATABASE


class ConnectionString(NamedTuple):
    """Connection string for neo4j."""
    user: str
    passwd: str
    host: str
    port: int
    database: str = DEFAULT_DATABASE


@contextmanager
def database(connection_string: ConnectionString) -> Session:
    """
    Context manager to get a safe session.

    :param connection_string: Connection parameter and credentials.
    """
    driver = GraphDatabase.driver(
        f"bolt://{connection_string.host}:{connection_string.port}",
        auth=(connection_string.user, connection_string.passwd))
    try:
        yield driver.session(database=connection_string.database)
    finally:
        driver.close()
        del driver


def driver_session(connection_string: ConnectionString) -> Session:
    """
    Context manager to get a safe session.

    :param connection_string: Connection parameter and credentials.
    """
    return GraphDatabase.driver(
        f"bolt://{connection_string.host}:{connection_string.port}",
        auth=(connection_string.user, connection_string.passwd
              )).session(database=connection_string.database)


@contextmanager
def runner(session: Session):
    """
    Allow run multiples statements for the same transaction.

    :param session: Database session.
    """
    try:
        transactor = session.begin_transaction()
        yield transactor
    finally:
        transactor.commit()


def _execute(connection_string: ConnectionString,
             query: str,
             variables: Optional[Dict[str, Any]] = None) -> Iterator[Any]:
    """Yield the result of executing a command."""
    variables = variables or {}
    with database(connection_string) as session:
        result = session.run(query, **variables)
        yield from result
