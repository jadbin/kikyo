from pydantic import BaseModel, Field


class Topic(BaseModel):
    """
    定义topic信息
    """

    name: str = Field(
        title='topic名称',
    )

    data_model: str = Field(
        title='topic中的数据模型',
    )
