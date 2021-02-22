from typing import Type

from pydantic import BaseModel, Field

from kikyo.schema.data import DataModel


class Topic(BaseModel):
    """
    定义topic信息
    """

    name: str = Field(
        title='topic名称',
    )

    data_model: Type[DataModel] = Field(
        default=None,
        title='数据模型',
    )
