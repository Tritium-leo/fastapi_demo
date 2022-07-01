import datetime
import json


class MyJsonDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=MyJsonDecoder.from_dict)

    @staticmethod
    def from_dict(d):
        if d.get("__class__") == "datetime":
            return datetime.datetime.fromtimestamp(float(d.get("timestamp")))

        elif d.get("__class__") == "date":
            return datetime.date.fromtimestamp(float(d.get("timestamp")))
        return d


def json_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return {"__class__": "datetime", "timestamp": str(obj.timestamp())}
    elif isinstance(obj, datetime.date):
        return {"__class__": "date",
                "timestamp": str(datetime.datetime.strptime(obj.strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp())}


# just like json dumps
def dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None,
          sort_keys=False, **kw):
    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                      allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=json_encoder,
                      sort_keys=sort_keys, **kw)


# just like json loads
def loads(s, *, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
    return json.loads(s, cls=MyJsonDecoder, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
                      parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)


if __name__ == "__main__":
    test_data = {"a": 123, "b": "bc", "c": datetime.datetime.now(), "d": datetime.date.today(), "e": {"d": "123"},
                 "f": ["123", "456"]}
    print(test_data)
    # d = json.dumps(test_data, default=json_encoder)
    # print(d)
    # data2 = json.loads(d, cls=MyJsonDecoder)
    # print("----", data2)

    d = dumps(test_data)
    print(d)
    o2 = loads(d)
    print(o2)
