
from django.http import HttpResponse

from servers.singleton import AccessManager
from servers.models import AccessRequestFactory


def index(request):
    manager1 = AccessManager()
    manager2 = AccessManager()

    request_types = ["read", "write", "admin"]
    request_objects = []

    for access_type in request_types:
        access_request = AccessRequestFactory.create(
            access_type,
            "demo_user",
            "company_db",
        )

        manager1.record_access(access_request.get_info())
        request_objects.append(access_request)

    requests_html = "".join(
        f"<li>{item.get_info()}</li>"
        for item in request_objects
    )

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Управление доступом к БД</title>
    </head>
    <body>
        <h1>Система управления доступом к БД (DAM)</h1>

        <h2>Singleton — AccessManager</h2>
        <p>Первый ID: {id(manager1)}</p>
        <p>Второй ID: {id(manager2)}</p>
        <p>Один экземпляр: {manager1 is manager2}</p>

        <h2>Factory — AccessRequestFactory</h2>
        <ul>{requests_html}</ul>

        <p><a href="/servers/list/">Открыть журнал доступа</a></p>
    </body>
    </html>
    """

    return HttpResponse(html)


def server_list(request):
    manager = AccessManager()
    log_html = "".join(
        f"<li>{entry}</li>"
        for entry in manager.get_access_log()
    )

    if not log_html:
        log_html = "<li>Запросов пока нет</li>"

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Журнал доступа</title>
    </head>
    <body>
        <h1>Журнал запросов доступа</h1>
        <ul>{log_html}</ul>
        <p><a href="/servers/">На главную</a></p>
    </body>
    </html>
    """

    return HttpResponse(html)
