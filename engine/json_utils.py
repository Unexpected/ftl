import json
from db.model import *


class Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        return obj
        #type = obj['_type']
        # if type == 'datetime':
        #    return parser.parse(obj['value'])
        # return obj


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Module):
            return {
                obj.name: str(obj.__dict__)
            }
        return super(Encoder, self).default(obj)
