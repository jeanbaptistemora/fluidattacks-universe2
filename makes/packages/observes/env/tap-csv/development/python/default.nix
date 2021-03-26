{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-csv-development-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "pytest==5.2.0"
    ];
    inherited = [
      "atomicwrites==1.4.0"
      "attrs==20.3.0"
      "more-itertools==8.7.0"
      "packaging==20.9"
      "pluggy==0.13.1"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "wcwidth==0.2.5"
    ];
  };
  python = nixpkgs.python38;
}
