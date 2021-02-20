from abc import ABCMeta
from typing import Union

from kikyo.nsclient import NamespacedClient
from kikyo.schema.topic import TopicModel


class FullTextClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供全文检索服务
    """

    def query(self, topic: Union[str, TopicModel]):
        """
        对指定topic构建查询。

        :param topic: 数据所在的topic
        """
