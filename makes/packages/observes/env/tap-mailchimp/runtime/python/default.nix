{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-mailchimp-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "mailchimp-marketing==3.0.31"
      "ratelimiter==1.2.0"
    ];
    inherited = [
      "bugsnag==4.0.2"
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "idna==2.10"
      "python-dateutil==2.8.1"
      "requests==2.25.1"
      "six==1.15.0"
      "urllib3==1.26.3"
      "WebOb==1.8.7"
    ];
  };
  python = nixpkgs.python38;
}
