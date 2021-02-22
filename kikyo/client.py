import base64
import importlib
import io
from typing import List, Optional

import pkg_resources
import requests
import yaml
from packaging import version

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
        return self

    def _init_plugins(self):
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

    def login(self, access_key: str, secret_key: str) -> 'Kikyo':
        """
        用户登录

        :param access_key: 用户名
        :param secret_key: 密码
        """


def configure_by_consul(config_url: str) -> Kikyo:
    """
    从Consul拉取YAML格式的配置文件

    :param config_url: 获取配置项的URL地址
    """

    resp = requests.get(config_url)
    resp.raise_for_status()

    ver = pkg_resources.get_distribution('kikyo')
    since: Optional[str] = None
    conf = None
    for data in resp.json():
        s = base64.b64decode(data['Value'])
        _conf = yaml.safe_load(io.BytesIO(s))
        _since = _conf.get('since', default='0')
        if since is None or version.parse(ver) >= version.parse(_since) > version.parse(since):
            since = _since
            conf = _conf

    plugins: Optional[List[dict]] = conf.get('plugins')
    if plugins:
        for kwargs in plugins:
            install_package(**kwargs)
    importlib.reload(pkg_resources)

    settings = conf.get('settings')
    return Kikyo(settings)
