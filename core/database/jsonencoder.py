from json import JSONEncoder, dumps
from pydantic import BaseModel


class PydanticJSONEncoder(JSONEncoder):

    def default(self, o: object):
        if isinstance(o, BaseModel):
            return o.model_dump()


def custom_serializer(obj):
    return dumps(obj, cls=PydanticJSONEncoder)
