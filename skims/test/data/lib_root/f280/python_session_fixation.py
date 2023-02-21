# pylint: skip-file
from testdjango.http import (  # noqa
    HttpRequest,
    HttpResponse,
)


def unsafe_values(request: HttpRequest) -> HttpResponse:
    value = request.GET.get("value")
    response = HttpResponse("")
    response["Set-Cookie"] = value  # Noncompliant
    response.set_cookie("sessionid", value)  # Noncompliant
    return response


def safe_values(request: HttpRequest, cookie: str) -> HttpResponse:
    value = request.GET.get("value")
    response = HttpResponse("")
    response["X-Data"] = value
    response["Set-Cookie"] = cookie
    response.set_cookie("data", value)
    response.set_cookie("sessionid", cookie)
    return response
