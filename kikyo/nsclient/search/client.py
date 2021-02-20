from abc import ABCMeta

from kikyo.nsclient import NamespacedClient


class SearchClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供全文检索服务
    """

    def query(self, topic: str):
        """
        对指定topic构建查询。

        :param topic: 数据所在的topic
        """
