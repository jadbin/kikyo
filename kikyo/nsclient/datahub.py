from abc import ABCMeta

from kikyo.nsclient import NamespacedClient


class DataHubClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供数据总线服务
    """
