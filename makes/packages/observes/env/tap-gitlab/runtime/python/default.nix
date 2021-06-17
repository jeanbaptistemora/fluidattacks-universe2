{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-gitlab-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.8.2087641"
      "aiohttp==3.6.2"
      "asgiref==3.2.10"
      "python-dateutil==2.8.1"
      "requests==2.25.1"
      "returns==0.16.0"
    ];
    inherited = [
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "certifi==2021.5.30"
      "chardet==3.0.4"
      "idna==3.1"
      "multidict==4.7.6"
      "six==1.16.0"
      "typing-extensions==3.10.0.0"
      "urllib3==1.26.5"
      "uvloop==0.14.0"
      "yarl==1.6.3"
    ];
  };
  python = nixpkgs.python38;
}
