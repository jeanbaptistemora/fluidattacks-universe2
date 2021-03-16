{ nixpkgs
, makeDerivation
, buildPythonRequirements
, path
, ...
} @ _:
let
  pythonRequirements = buildPythonRequirements {
    name = "integrates-back-security-python";
    python = nixpkgs.python37;
    requirements = {
      direct = [
        "bandit==1.6.2"
      ];
      inherited = [
        "gitdb==4.0.5"
        "GitPython==3.1.14"
        "importlib-metadata==3.7.3"
        "pbr==5.5.1"
        "PyYAML==5.4.1"
        "six==1.15.0"
        "smmap==3.0.5"
        "stevedore==3.3.0"
        "typing-extensions==3.7.4.3"
        "zipp==3.4.1"
      ];
    };
  };
in
makeDerivation {
  arguments = {
    envSrcIntegratesBack = path "/integrates/back";
  };
  builder = path "/makes/packages/integrates/back/security/builder.sh";
  name = "integrates-back-security";
  searchPaths = {
    envPaths = [
      pythonRequirements
    ];
    envPython37Paths = [
      pythonRequirements
    ];
  };
}
