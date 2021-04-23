{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-mailchimp-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "mailchimp-marketing==3.0.40"
      "ratelimiter==1.2.0.post0"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "idna==2.10"
      "python-dateutil==2.8.1"
      "requests==2.25.1"
      "six==1.15.0"
      "urllib3==1.26.4"
    ];
  };
  python = nixpkgs.python38;
}
