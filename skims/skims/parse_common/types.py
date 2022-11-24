from collections import (
    UserDict,
    UserList,
    UserString,
)
from typing import (
    Any,
    Iterable,
    Union,
)


class StringToken(UserString):
    def __init__(
        self,
        value: str,
        line: int,
        column: int,
    ):
        super().__init__(value)
        self.__column__ = column
        self.__line__ = line


class FloatToken(float):
    def __new__(  # type: ignore
        cls,
        value: Union[float, str, int],
        column: int,  # pylint: disable=unused-argument
        line: int,  # pylint: disable=unused-argument
    ) -> float:
        return float.__new__(cls, value)

    def __init__(
        self,
        value: Union[float, str, int],
        column: int,
        line: int,
    ):
        float.__init__(float(value))
        self.__column__ = column
        self.__line__ = line


class IntToken(int):
    def __new__(  # type: ignore
        cls,
        value: Union[float, str, int],
        column: int,  # pylint: disable=unused-argument
        line: int,  # pylint: disable=unused-argument
    ) -> int:
        return int.__new__(cls, value)

    def __init__(
        self,
        value: Union[float, str, int],
        column: int,
        line: int,
    ):
        int.__init__(int(value))
        self.__column__ = column
        self.__line__ = line


class ListToken(UserList):
    def __init__(
        self,
        value: Iterable[Any],
        line: int = 0,
        column: int = 0,
    ):
        super().__init__(value)
        self.__line__ = line
        self.__column__ = column


class TupleToken(tuple):
    def __new__(  # type: ignore
        cls,
        value: Iterable[Any],
        column: int,  # pylint: disable=unused-argument
        line: int,  # pylint: disable=unused-argument
    ) -> int:
        return tuple.__new__(cls, value)  # type: ignore

    def __init__(
        self,
        value: tuple,
        column: int,
        line: int,
    ):
        tuple.__init__(value)
        self.__column__ = column
        self.__line__ = line


class DictToken(UserDict):
    def __init__(
        self,
        value: dict,
        column: int,
        line: int,
    ):
        super().__init__(value)
        self.__column__ = column
        self.__line__ = line
