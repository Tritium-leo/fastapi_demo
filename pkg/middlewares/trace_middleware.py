import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware


class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = request.headers.get("X-TRACE-ID", None)
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        if trace_id is None:
            response.headers.setdefault("X-TRACE-ID", str(uuid.uuid4()))
        else:
            response.headers.setdefault("X-TRACE-ID", trace_id)
        response.headers["X-DURATION"] = f"{round(end_time - start_time, 3)}"
        return response
