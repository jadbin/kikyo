from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, List

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


class Query(metaclass=ABCMeta):
    """
    构建面向topic的查询
    """

    _filters: List[FilterClause]

    def filter(self, name: str) -> 'FilterBuilder':
        """
        基于筛选表达式检索数据

        :param name: 筛选的字段名称
        """

        return FilterBuilder(name, self)

    @abstractmethod
    def nested(self, name: str, query: 'Query') -> 'Query':
        """
        嵌套查询

        :param name: 字段名称
        :param query: 查询
        """

    @abstractmethod
    def paginate(self, page: int = 0, size: int = 10) -> 'Query':
        """
        分页查询

        :param page: 分页的页码，从0开始
        :param size: 分页的大小
        """

    @abstractmethod
    def all(self, as_model=False) -> List[dict]:
        """
        返回命中查询的所有数据，默认进行了分页。
        """

    @abstractmethod
    def first(self, as_model=False) -> dict:
        """
        返回命中查询的第一条数据
        """


class FilterBuilder:
    def __init__(self, name: str, query: Query):
        self._name = name
        self._query = query

    def is_(self, value: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS,
                name=self._name,
                value=value,
            )
        )
        return self._query

    def is_not(self, value: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_NOT,
                name=self._name,
                value=value
            )
        )
        return self._query

    def is_one_of(self, *values: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_ONE_OF,
                name=self._name,
                value=list(values)
            )
        )
        return self._query

    def is_not_one_of(self, *values: Any) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_NOT_ONE_OF,
                name=self._name,
                value=list(values)
            )
        )
        return self._query

    def is_between(self, lower_bound: Any = None, upper_bound: Any = None) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_BETWEEN,
                name=self._name,
                value=(lower_bound, upper_bound),
            )
        )
        return self._query

    def is_not_between(self, lower_bound: Any = None, upper_bound: Any = None) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.IS_NOT_BETWEEN,
                name=self._name,
                value=(lower_bound, upper_bound),
            )
        )
        return self._query

    def exists(self) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.EXISTS,
                name=self._name,
            )
        )
        return self._query

    def does_not_exists(self) -> Query:
        self._query._filters.append(
            FilterClause(
                type=FilterType.DOES_NOT_EXIST,
                name=self._name,
            )
        )
        return self._query


class Index(metaclass=ABCMeta):
    """
    索引
    """

    @abstractmethod
    def exists(self, _id: str) -> bool:
        """
        指定ID的数据是否存在

        :param _id: 数据ID
        """

    @abstractmethod
    def get(self, _id: str) -> dict:
        """
        返回指定数据

        :param _id: 数据的ID
        """

    @abstractmethod
    def put(self, _id: str, data: dict):
        """
        更新指定数据，指定ID不存在时自动创建数据

        :param _id: 数据ID
        :param data: 数据内容
        """

    @abstractmethod
    def delete(self, _id: str):
        """
        删除指定数据

        :param _id: 数据ID
        """


class SearchClient(metaclass=ABCMeta):
    """
    提供全文检索服务
    """

    @abstractmethod
    def query(self, topic: str) -> Query:
        """
        对指定topic构建查询

        :param topic: topic名称
        """

    @abstractmethod
    def index(self, topic: str) -> Index:
        """
        对指定topic返回索引

        :param topic: topic名称
        """
