from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from jose import jwt

class Request:

    def get_request(self, data_user):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = data_user['username']
        request.session['company'] = data_user['company']
        request.session['role'] = data_user['role']
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': data_user['useremail'],
                'user_role': data_user['role'],
                'company': data_user['company']
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )

        return request