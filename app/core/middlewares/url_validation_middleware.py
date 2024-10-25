import re
import urllib.parse
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.constant import AppStatus

# Regular expression for allowed characters in the path and query
ALLOWED_PATH_CHARS = re.compile(r'^[a-zA-Z0-9/_\-\.]*$')
ALLOWED_QUERY_CHARS = re.compile(r'^[a-zA-Z0-9/_\-\.&=% \u00C0-\u024F\u1E00-\u1EFF{}":,]*$')


class URLValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Parse the full URL including the query parameters
        parsed_url = urllib.parse.urlparse(request.url._url)
        decoded_path = urllib.parse.unquote(parsed_url.path)
        decoded_query = urllib.parse.unquote(parsed_url.query)

        # Validate the decoded URL path and query
        if not ALLOWED_PATH_CHARS.match(decoded_path):
            return JSONResponse(
                status_code=403,
                content={
                    "detail": {
                        "name": AppStatus.ERROR_400_INVALID_URL.name,
                        "message": AppStatus.ERROR_400_INVALID_URL.message,
                    }
                }
            )

        # Remove 'filename' from query parameters
        query_params = urllib.parse.parse_qs(decoded_query)
        does_filename_in_query = False
        filtered_query_params = {}
        for k, v in query_params.items():
            if k != "filename":
                filtered_query_params[k] = v
            else:
                does_filename_in_query = True

        if does_filename_in_query:
            filtered_query_string = urllib.parse.urlencode(filtered_query_params, doseq=True)
            decoded_query = urllib.parse.unquote(filtered_query_string).replace('+', ' ')

        if not ALLOWED_QUERY_CHARS.match(decoded_query):
            return JSONResponse(
                status_code=403,
                content={
                    "detail": {
                        "name": AppStatus.ERROR_400_INVALID_URL.name,
                        "message": AppStatus.ERROR_400_INVALID_URL.message,
                    }
                }
            )

        # Update the request URL with the validated URL components
        request._url = request.url.replace(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            path=decoded_path,
            query=decoded_query,
            fragment=parsed_url.fragment,
        )

        response = await call_next(request)
        return response
