{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-streamer-zoho-crm-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "ratelimiter==1.2.0.post0"
      "requests==2.25.1"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "idna==2.10"
      "urllib3==1.26.4"
    ];
  };
  python = nixpkgs.python38;
}
