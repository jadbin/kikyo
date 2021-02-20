from typing import Union

from kikyo.schema.filter import FilterClause
from kikyo.schema.topic import TopicModel


class Query:
    def __init__(self, topic: Union[str, TopicModel]):
        """
        构建面向topic的查询。

        :param topic: topic的名称
        """

    def get(self, data_id: str):
        """
        返回指定数据

        :param data_id: 数据的ID
        """

    def filter(self, *clauses: FilterClause):
        """
        基于筛选表达式检索数据。

        :param clauses: 构建的筛选表达式。
        """

    def paginate(self, page: int = 0, size: int = 10):
        """
        分页查询

        :param page: 分页的页码，从0开始
        :param size: 分页的大小
        """

    def all(self):
        """
        返回命中查询的所有数据，默认进行了分页。
        """

    def first(self):
        """
        返回命中查询的第一条数据
        """
