from fluidasserts.proto import http

URL = 'http://testphp.vulnweb.com/guestbook.php'
BAD_TEXT = r'<script>alert\("Hacked by FLUIDAttacks"\);<\/script>'
DATA = {
    'name': 'anonymous user',
    'submit': 'add message',
    'text': '<script>alert("Hacked by FLUIDAttacks");</script>'
}

http.has_xss(URL, BAD_TEXT, data=DATA)