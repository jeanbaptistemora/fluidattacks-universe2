{ observesPkgs
, ...
} @ _:
let
  buildPythonRequirements = import ../../../../../makes/utils/build-python-requirements observesPkgs;
in
buildPythonRequirements {
  dependencies = [
  ];
  requirements = {
    direct = [
      "click==7.1.2"
      "ratelimiter==1.2.0"
      "requests==2.25.0"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==3.0.4"
      "idna==2.10"
      "urllib3==1.26.2"
    ];
  };
  python = observesPkgs.python38;
}
