import json
from sqlalchemy import inspect


class Utils:
    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}

    def orm_to_json(self, obj):
        if isinstance(obj, list):
            json_data = []
            for o in obj:
                json_data.append(self.object_as_dict(o))
            return json.dumps(json_data, ensure_ascii=False).encode('utf8')
        else:
            return json.dumps(self.object_as_dict(obj), ensure_ascii=False).encode('utf8')