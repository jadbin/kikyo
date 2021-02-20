import base64
import io

import requests
import yaml

from kikyo.nsclient.file import FileClient
from kikyo.nsclient.message import MessageClient
from kikyo.nsclient.search import SearchClient
from kikyo.settings import Settings


class Kikyo:
    settings: Settings

    message: MessageClient
    file: FileClient
    search: SearchClient

    def __init__(self, settings: dict = None):
        self._init(settings)

    def _init(self, settings):
        if settings is None:
            return

        self.settings = None if settings is None else Settings(settings)

        if 'access_key' in self.settings and 'secret_key' in self.settings:
            self.login(self.settings['access_key'], self.settings['secret_key'])

    def use_consul_config(
            self,
            config_url: str,
    ) -> 'Kikyo':
        """
        从Consul拉取YAML格式的配置文件

        :param config_url: 获取配置项的URL地址
        """

        resp = requests.get(config_url)
        resp.raise_for_status()

        data = resp.json()[0]['Value']
        s = base64.b64decode(data)
        settings = yaml.safe_load(io.BytesIO(s))

        self._init(settings)
        return self

    def login(self, access_key: str, secret_key: str):
        """
        用户登录

        :param access_key: 用户名
        :param secret_key: 密码
        :return:
        """

    def self_space(self):
        """
        使用个人空间。
        """
