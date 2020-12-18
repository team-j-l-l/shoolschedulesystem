from datetime import datetime, date
from decimal import Decimal
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)

        return json.JSONEncoder.default(self, o)


def json_dumps(obj):
    return json.dumps(obj, cls=JSONEncoder)

def json_loads(s):
    return json.loads(s)
