from abc import ABCMeta
from enum import Enum
from typing import Any

from pydantic import BaseModel


class FilterType(Enum):
    IS = 1
    IS_NOT = 2
    IS_ONE_OF = 3
    IS_NOT_ONE_OF = 4
    IS_BETWEEN = 5
    IS_NOT_BETWEEN = 6
    EXISTS = 7
    DOES_NOT_EXIST = 8


class FilterClause(BaseModel):
    type: FilterType
    name: str
    value: Any = None


class FilterableField:
    __field_name__: str

    def is_(self, value: Any) -> FilterClause:
        return FilterClause(
            type=FilterType.IS,
            name=self.__field_name__,
            value=value
        )

    def is_not(self, value: Any) -> FilterClause:
        return FilterClause(
            type=FilterType.IS_NOT,
            name=self.__field_name__,
            value=value
        )

    def is_one_of(self, *values: Any) -> FilterClause:
        return FilterClause(
            type=FilterType.IS_ONE_OF,
            name=self.__field_name__,
            value=list(values)
        )

    def is_not_one_of(self, *values: Any) -> FilterClause:
        return FilterClause(
            type=FilterType.IS_NOT_ONE_OF,
            name=self.__field_name__,
            value=list(values)
        )

    def is_between(self, lower_bound: Any = None, upper_bound: Any = None) -> FilterClause:
        return FilterClause(
            type=FilterType.IS_BETWEEN,
            name=self.__field_name__,
            value=(lower_bound, upper_bound),
        )

    def is_not_between(self, lower_bound: Any = None, upper_bound: Any = None) -> FilterClause:
        return FilterClause(
            type=FilterType.IS_NOT_BETWEEN,
            name=self.__field_name__,
            value=(lower_bound, upper_bound),
        )

    def exists(self) -> FilterClause:
        return FilterClause(
            type=FilterType.EXISTS,
            name=self.__field_name__,
        )

    def does_not_exists(self) -> FilterClause:
        return FilterClause(
            type=FilterType.DOES_NOT_EXIST,
            name=self.__field_name__,
        )


class FilterableModelMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        for k, v in cls.__dict__.items():
            if isinstance(v, FilterableField):
                v.__field_name__ = k

        return cls


class FilterableModel(metaclass=FilterableModelMeta):
    pass
