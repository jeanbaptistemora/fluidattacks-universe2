{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-code-etl-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.11.1621472"
      "click==7.1.2"
      "GitPython==3.1.14"
      "ratelimiter==1.2.0.post0"
      "requests==2.25.1"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "gitdb==4.0.7"
      "idna==2.10"
      "smmap==4.0.0"
      "urllib3==1.26.4"
    ];
  };
  python = nixpkgs.python38;
}
