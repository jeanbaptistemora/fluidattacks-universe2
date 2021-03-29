{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-streamer-zoho-crm-development-python";
  requirements = {
    direct = [
      "pytest-postgresql==2.5.2"
      "pytest==5.2.0"
    ];
    inherited = [
      "atomicwrites==1.4.0"
      "attrs==20.3.0"
      "mirakuru==2.3.0"
      "more-itertools==8.7.0"
      "packaging==20.9"
      "pluggy==0.13.1"
      "port-for==0.4"
      "psutil==5.8.0"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "wcwidth==0.2.5"
    ];
  };
  python = nixpkgs.python38;
}
