from abc import ABCMeta, abstractmethod
from typing import Union, Any

from kikyo.nsclient import NamespacedClient
from kikyo.schema.topic import Topic


class Producer(metaclass=ABCMeta):
    """
    生产者
    """

    def __enter__(self) -> 'Producer':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def send(self, *records: Any):
        """
        发送数据

        :param records: 数据
        """

    def close(self):
        """
        关闭生产者
        """


class Consumer(metaclass=ABCMeta):
    """
    消费者
    """

    def __enter__(self) -> 'Consumer':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def receive(self, limit=1) -> Any:
        """
        接收数据

        :param limit: 限制接收数据的数量
        """

    def close(self):
        """
        关闭消费者
        """


class DataHubClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供数据总线服务
    """

    @abstractmethod
    def create_producer(self, topic: Union[Topic, str]) -> Producer:
        """
        创建向指定topic发送数据的生产者

        :param topic: topic名称
        """

    @abstractmethod
    def subscribe(
            self,
            topic: Union[Topic, str],
            subscription_name: str = None,
    ) -> Consumer:
        """
        订阅指定topic

        :param topic: topic名称
        :param subscription_name: 订阅的标识
        """
