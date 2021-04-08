{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-formstack-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "delighted==4.0.0"
      "returns==0.16.0"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "idna==2.10"
      "pytz==2021.1"
      "requests==2.25.1"
      "six==1.15.0"
      "typing-extensions==3.7.4.3"
      "tzlocal==2.1"
      "urllib3==1.26.4"
    ];
  };
  python = nixpkgs.python38;
}
