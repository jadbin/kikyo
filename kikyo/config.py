import base64
import io

import requests
import yaml


def configure_by_consul(config_url: str) -> dict:
    """
    从Consul拉取YAML格式的配置文件

    :param config_url: 获取配置项的URL地址
    """

    resp = requests.get(config_url)
    resp.raise_for_status()

    data = resp.json()[0]
    s = base64.b64decode(data['Value'])
    conf = yaml.safe_load(io.BytesIO(s))

    settings = conf.get('kikyo')
    return settings
