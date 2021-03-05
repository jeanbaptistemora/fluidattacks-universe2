{ assertsPkgs
, buildPythonRequirements
, ...
}:
buildPythonRequirements {
  name = "asserts-pypi-runtime";
  python = assertsPkgs.python37;
  requirements = {
    direct = [
      "aiohttp==3.6.2"
      "androguard==3.3.5"
      "azure-common==1.1.25"
      "azure-identity==1.3.1"
      "azure-keyvault==4.1.0"
      "azure-mgmt-compute==13.0.0"
      "azure-mgmt-keyvault==2.2.0"
      "azure-mgmt-network==11.0.0"
      "azure-mgmt-resource==10.1.0"
      "azure-mgmt-security==0.4.1"
      "azure-mgmt-sql==0.20.0"
      "azure-mgmt-storage==11.1.0"
      "azure-mgmt-web==0.47.0"
      "azure-storage-file==2.1.0"
      "bandit==1.6.2"
      "bcrypt==3.1.7"
      "beautifulsoup4==4.9.1"
      "boto3==1.14.32"
      "certifi==2020.6.20"
      "cffi==1.14.2"
      "cfn-flip==1.2.3"
      "colorama==0.4.3"
      "configobj==5.0.6"
      "cryptography==3.0"
      "Cython==0.29.21"
      "defusedxml==0.6.0"
      "dnspython==1.16.0"
      "docker==4.2.2"
      "GitPython==3.1.7"
      "google-api-python-client==1.10.0"
      "google-auth-httplib2==0.0.4"
      "jmespath==0.10.0"
      "kubernetes==11.0.0"
      "lark-parser==0.9.0"
      "ldap3==2.7"
      "mitmproxy==5.0.1"
      "mixpanel==4.6.0"
      "names==0.3.0"
      "networkx==2.4"
      "ntplib==0.3.4"
      "oyaml==0.9"
      "paramiko==2.7.1"
      "Pillow==7.2.0"
      "PyDriller==1.15.2"
      "Pygments==2.6.1"
      "pyhcl==0.4.4"
      "pyjks==20.0.0"
      "PyJWT==1.7.1"
      "PyNaCl==1.4.0"
      "pyOpenSSL==19.1.0"
      "pyparsing==2.4.7"
      "PyPDF2==1.26.0"
      "pysmb==1.2.1"
      "pytesseract==0.3.4"
      "python-dateutil==2.8.1"
      "python-magic==0.4.18"
      "pytz==2020.1"
      "pywinrm==0.4.1"
      "requests-ntlm==1.1.0"
      "requests==2.24.0"
      "requirements-detector==0.7"
      "selenium==3.141.0"
      "tlslite-ng==0.8.0a38"
      "typed-ast==1.4.1"
      "viewstate==0.5.3"
    ];
    inherited = [
      "adal==1.2.6"
      "asn1crypto==1.4.0"
      "astroid==2.5"
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "azure-core==1.11.0"
      "azure-keyvault-certificates==4.2.1"
      "azure-keyvault-keys==4.3.1"
      "azure-keyvault-secrets==4.2.0"
      "azure-storage-common==2.1.0"
      "backcall==0.2.0"
      "blinker==1.4"
      "botocore==1.17.63"
      "Brotli==1.0.9"
      "cachetools==4.2.1"
      "chardet==3.0.4"
      "click==7.1.2"
      "cycler==0.10.0"
      "decorator==4.4.2"
      "docutils==0.15.2"
      "ecdsa==0.16.1"
      "Flask==1.1.2"
      "future==0.18.2"
      "gitdb==4.0.5"
      "google-api-core==1.26.0"
      "google-auth==1.27.0"
      "googleapis-common-protos==1.52.0"
      "h11==0.12.0"
      "h2==3.2.0"
      "hpack==3.0.0"
      "httplib2==0.19.0"
      "hyperframe==5.2.0"
      "idna==2.10"
      "importlib-metadata==3.5.0"
      "ipython-genutils==0.2.0"
      "ipython==7.20.0"
      "isodate==0.6.0"
      "itsdangerous==1.1.0"
      "javaobj-py3==0.4.2"
      "jedi==0.18.0"
      "Jinja2==2.11.3"
      "kaitaistruct==0.8"
      "kiwisolver==1.3.1"
      "lazy-object-proxy==1.5.2"
      "lizard==1.17.7"
      "lxml==4.6.2"
      "MarkupSafe==1.1.1"
      "matplotlib==3.3.4"
      "msal-extensions==0.1.3"
      "msal==1.9.0"
      "msrest==0.6.21"
      "msrestazure==0.6.4"
      "multidict==4.7.6"
      "ntlm-auth==1.5.0"
      "numpy==1.20.1"
      "oauthlib==3.1.0"
      "packaging==20.9"
      "parso==0.8.1"
      "passlib==1.7.4"
      "pbr==5.5.1"
      "pexpect==4.8.0"
      "pickleshare==0.7.5"
      "portalocker==1.7.1"
      "prompt-toolkit==3.0.16"
      "protobuf==3.10.0"
      "ptyprocess==0.7.0"
      "publicsuffix2==2.20191221"
      "pyasn1-modules==0.2.8"
      "pyasn1==0.4.8"
      "pycparser==2.20"
      "pycryptodomex==3.10.1"
      "pydot==1.4.2"
      "pyperclip==1.7.0"
      "PyYAML==5.4.1"
      "requests-oauthlib==1.3.0"
      "rsa==4.7.1"
      "ruamel.yaml.clib==0.2.2"
      "ruamel.yaml==0.16.12"
      "s3transfer==0.3.4"
      "six==1.15.0"
      "smmap==3.0.5"
      "sortedcontainers==2.1.0"
      "soupsieve==2.2"
      "stevedore==3.3.0"
      "tornado==6.1"
      "traitlets==5.0.5"
      "twofish==0.3.0"
      "typing-extensions==3.7.4.3"
      "uritemplate==3.0.1"
      "urllib3==1.26.3"
      "urwid==2.0.1"
      "wcwidth==0.2.5"
      "websocket-client==0.57.0"
      "Werkzeug==1.0.1"
      "wrapt==1.12.1"
      "wsproto==0.14.1"
      "xmltodict==0.12.0"
      "yarl==1.6.3"
      "zipp==3.4.0"
      "zstandard==0.12.0"
    ];
  };
}
