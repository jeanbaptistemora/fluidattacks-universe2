{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-paginator-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.11.1621472"
      "Deprecated==1.2.12"
      "requests==2.25.1"
      "returns==0.16.0"
    ];
    inherited = [
      "certifi==2021.5.30"
      "chardet==4.0.0"
      "idna==2.10"
      "typing-extensions==3.7.4.3"
      "urllib3==1.26.6"
      "wrapt==1.12.1"
    ];
  };
  python = nixpkgs.python38;
}
