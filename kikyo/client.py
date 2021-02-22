import base64
import io

import pkg_resources
import requests
import yaml

from kikyo.nsclient.datahub import DataHubClient
from kikyo.nsclient.files import FilesClient
from kikyo.nsclient.search import SearchClient
from kikyo.settings import Settings
from kikyo.utils import install_package


class Kikyo:
    datahub: DataHubClient
    files: FilesClient
    search: SearchClient

    settings: Settings

    def __init__(self, settings: dict = None):
        if settings is not None:
            self.init(settings)

    def init(self, settings) -> 'Kikyo':
        self.settings = Settings(settings)

        self._init_plugins()

        if 'access_key' in self.settings and 'secret_key' in self.settings:
            self.login(self.settings['access_key'], self.settings['secret_key'])

        return self

    def _init_plugins(self):
        plugins_config = self.settings.get('plugins', default={})
        self._install_plugins(plugins_config)

        plugins = {
            entry_point.name: entry_point.load()
            for entry_point in pkg_resources.iter_entry_points('kikyo.plugins')
        }

        active_plugins = self.settings.getlist('active_plugins')
        if active_plugins:
            active_plugins = set(active_plugins)
            for name in list(plugins.keys()):
                if name not in active_plugins:
                    del plugins[name]

        for name, plugin in plugins.items():
            if hasattr(plugin, 'configure_kikyo'):
                plugin.configure_kikyo(self)

    @staticmethod
    def _install_plugins(config: dict):
        for name, conf in config.items():
            pkg = conf.get('package')
            min_ver = conf.get('min_ver')
            max_ver = conf.get('max_ver')
            index_url = conf.get('index_url')
            install_package(pkg, min_ver=min_ver, max_ver=max_ver, index_url=index_url)

    def init_by_consul(self, config_url: str) -> 'Kikyo':
        """
        从Consul拉取YAML格式的配置文件

        :param config_url: 获取配置项的URL地址
        """

        resp = requests.get(config_url)
        resp.raise_for_status()

        data = resp.json()[0]['Value']
        s = base64.b64decode(data)
        settings = yaml.safe_load(io.BytesIO(s))

        self.init(settings)
        return self

    def login(self, access_key: str, secret_key: str) -> 'Kikyo':
        """
        用户登录

        :param access_key: 用户名
        :param secret_key: 密码
        """
