from abc import ABCMeta

from kikyo.nsclient import NamespacedClient


class MessageClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供消息队列服务
    """
