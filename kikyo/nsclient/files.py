from abc import ABCMeta, abstractmethod

from kikyo.nsclient import NamespacedClient


class FilesClient(NamespacedClient, metaclass=ABCMeta):
    """
    提供文件存储服务
    """

    @abstractmethod
    def get_file_link(self, bucket: str, filename: str):
        """
        获取文件的下载链接。

        :param bucket: 文件所在bucket的名称
        :param filename: 文件名称
        """
