{ buildPythonRequirements
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "integrates-back-runtime";
    requirements = {
      direct = [
        "aioboto3==8.0.3"
        "aiodataloader==0.2.0"
        "aioextensions==20.8.2087641"
        "aiofiles==0.5.0"
        "amazon-dax-client==1.1.7"
        "ariadne[asgi-file-uploads]==0.12.0"
        "asgiref==3.2.10"
        "async-lru==1.0.2"
        "Authlib==0.15.1"
        "awscli==1.18.76"
        "backports.csv==1.0.7"
        "boto3-type-annotations==0.3.1"
        "boto3==1.13.26"
        "botocore==1.16.26"
        "bugsnag==4.0.1"
        "channels==3.0.0"
        "cloudmersive-virus-api-client==2.0.6"
        "cryptography==3.2.1"
        "exponent-server-sdk==0.3.1"
        "fpdf==1.7.2"
        "frozendict==1.2"
        "GitPython==3.1.11"
        "graphql-core==3.0.3"
        "gunicorn==20.0.4"
        "httplib2==0.18.1"
        "httpx==0.16.1"
        "hyperlink==19.0.0"
        "idna==2.9"
        "itsdangerous==1.1.0"
        "Jinja2==2.11.2"
        "jwcrypto==0.8"
        "lxml==4.5.2"
        "mandrill-really-maintained==1.2.4"
        "matplotlib==3.2.1"
        "mixpanel==4.5.0"
        "newrelic==5.22.1.152"
        "oauth2client==4.1.3"
        "Pillow==7.2.0"
        "PyExcelerate==0.9.0"
        "pykwalify==1.7.0"
        "PyPDF4==1.27.0"
        "python-jose==3.1.0"
        "python-magic==0.4.18"
        "python-multipart==0.0.5"
        "pytz==2020.1"
        "redis-py-cluster==2.1.0"
        "redis==3.5.3"
        "retrying==1.3.3"
        "s3transfer==0.3.3"
        "simplejson==3.17.0"
        "social-auth-core==3.3.3"
        "starlette==0.13.8"
        "tracers==20.7.1645"
        "uvicorn[standard]==0.12.3"
        "watchtower==0.7.3"
        "zenpy==2.0.20"
      ];
      inherited = [
        "aiobotocore==1.0.4"
        "aiogqlc==1.0.5"
        "aiohttp==3.7.3"
        "aioitertools==0.7.1"
        "antlr4-python3-runtime==4.7.2"
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "autobahn==21.2.1"
        "Automat==20.2.0"
        "cachetools==4.2.1"
        "certifi==2020.12.5"
        "cffi==1.14.5"
        "chardet==4.0.0"
        "click==7.1.2"
        "colorama==0.4.3"
        "constantly==15.1.0"
        "cycler==0.10.0"
        "daphne==3.0.1"
        "defusedxml==0.7.0rc2"
        "Django==3.1.6"
        "docopt==0.6.2"
        "docutils==0.15.2"
        "ecdsa==0.16.1"
        "gitdb==4.0.5"
        "h11==0.12.0"
        "httpcore==0.12.3"
        "httptools==0.1.1"
        "incremental==17.5.0"
        "jmespath==0.10.0"
        "kiwisolver==1.3.1"
        "MarkupSafe==1.1.1"
        "more-itertools==8.4.0"
        "multidict==5.1.0"
        "numpy==1.20.1"
        "oauthlib==3.1.0"
        "pyasn1-modules==0.2.8"
        "pyasn1==0.4.8"
        "pycparser==2.20"
        "PyHamcrest==2.0.2"
        "PyJWT==2.0.1"
        "pyOpenSSL==20.0.1"
        "pyparsing==2.4.7"
        "python-dateutil==2.8.1"
        "python-dotenv==0.15.0"
        "python3-openid==3.2.0"
        "PyYAML==5.4.1"
        "requests-oauthlib==1.3.0"
        "requests==2.25.1"
        "rfc3986==1.4.0"
        "rsa==3.4.2"
        "service-identity==18.1.0"
        "six==1.15.0"
        "smmap==3.0.5"
        "sniffio==1.2.0"
        "sqlparse==0.4.1"
        "Twisted==20.3.0"
        "txaio==20.12.1"
        "typing-extensions==3.7.4.3"
        "urllib3==1.26.4"
        "uvloop==0.15.1"
        "watchgod==0.6"
        "WebOb==1.8.6"
        "websockets==8.1"
        "wrapt==1.12.1"
        "yarl==1.6.3"
        "zope.interface==5.2.0"
      ];
    };
    python = nixpkgs.python37;
  };
in
makeTemplate {
  name = "integrates-back-pypi-runtime";
  searchPaths = {
    envPaths = [
      pythonRequirements
    ];
    envPythonPaths = [
      (path "/integrates/back/packages/modules")
      (path "/integrates/back/packages/integrates-back")
      (path "/integrates")
    ];
    envPython37Paths = [
      pythonRequirements
    ];
    envSources = [
      packages.makes.python.safe-pickle
    ];
  };
}
