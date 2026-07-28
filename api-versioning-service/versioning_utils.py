from functools import wraps

from flask import jsonify, make_response, request


def deprecated_version(sunset_date):
    """
    Add standards-compatible deprecation information to an API response.

    Args:
        sunset_date: HTTP-date indicating when the version will be retired.
    """

    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            original_response = function(*args, **kwargs)
            response = make_response(original_response)

            response.headers["Deprecation"] = "true"
            response.headers["Sunset"] = sunset_date
            response.headers["Warning"] = (
                '299 - "API v1 is deprecated; migrate to API v2"'
            )

            return response

        return decorated_function

    return decorator


def version_response(data, version, status_code=200):
    """
    Return a JSON response containing an API-Version header.

    Args:
        data: JSON-serialisable response data.
        version: API version such as v1 or v2.
        status_code: HTTP response status code.
    """
    response = make_response(jsonify(data), status_code)
    response.headers["API-Version"] = version

    return response


def get_api_version(flask_request):
    """
    Determine the requested API version from the URL or request headers.
    """
    path_parts = flask_request.path.strip("/").split("/")

    if len(path_parts) >= 2 and path_parts[0] == "api":
        possible_version = path_parts[1]

        if possible_version.startswith("v"):
            return possible_version

    header_version = flask_request.headers.get("API-Version")

    if header_version:
        return header_version.strip().lower()

    return "v2"


def route_to_version(versions_map, default="v2"):
    """
    Call the handler associated with the requested API version.
    """
    requested_version = get_api_version(request) or default
    handler = versions_map.get(requested_version)

    if handler is None:
        return version_response(
            {
                "error": {
                    "code": "UNSUPPORTED_API_VERSION",
                    "message": f"API version '{requested_version}' is not supported",
                    "supported_versions": sorted(versions_map.keys()),
                }
            },
            requested_version,
            404,
        )

    return handler()
