from abc import ABCMeta, abstractmethod
from typing import Union

from kikyo.nsclient import NamespacedClient
from kikyo.nsclient.search.query import Query
from kikyo.schema.topic import Topic


class SearchClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供全文检索服务
    """

    @abstractmethod
    def query(self, topic: Union[Topic, str]) -> Query:
        """
        对指定topic构建查询。

        :param topic: topic名称
        """
