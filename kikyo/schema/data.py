import datetime as dt

from pydantic import BaseModel, Field


class DataMeta(BaseModel):
    """
    定义基础数据类型的元信息
    """

    create_time: dt.datetime = Field(
        default=None,
        title='数据创建时间',
    )


class DataModel(BaseModel):
    """
    定义基础数据类型
    """

    uid: str = Field(
        title='数据统一标识',
    )

    meta: DataMeta = Field(
        default=None,
        title='数据的元信息'
    )
