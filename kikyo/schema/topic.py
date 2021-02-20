from pydantic import BaseModel, Field

from kikyo.schema.filter import FilterableField, FilterableModel


class TopicModel(BaseModel, FilterableModel):
    """
    定义topic下的数据类型
    """

    __topic_name__: str


class TopicField(Field, FilterableField):
    """
    定义topic下数据类型的字段
    """
