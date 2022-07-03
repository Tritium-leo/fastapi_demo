import datetime
import json
import typing

from fastapi.responses import JSONResponse


def my_json_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.timestamp()
    elif isinstance(obj, datetime.date):
        return datetime.datetime.strptime(obj.strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp()


class JsonResponse(JSONResponse):

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=my_json_encoder
        ).encode("utf-8")
