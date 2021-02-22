import datetime as dt

from pydantic import BaseModel, Field


class DataModel(BaseModel):
    """
    定义基础数据类型的元信息
    """

    data_type: str

    data_uid: str = Field(
        title='数据统一标识',
    )

    create_time: dt.datetime = Field(
        default=None,
        title='数据创建时间',
    )
