{ forcesPkgs
, path
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path forcesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path forcesPkgs;
in
makeTemplate {
  arguments = {
    envPython = "${forcesPkgs.python38}/bin/python";
    envPythonRequirements = buildPythonRequirements {
      dependencies = [ ];
      name = "forces-wrapper";
      requirements = {
        direct = [
          "boto3==1.16.63"
          "click==7.1.2"
        ];
        inherited = [
          "botocore==1.19.63"
          "jmespath==0.10.0"
          "python-dateutil==2.8.1"
          "s3transfer==0.3.4"
          "six==1.15.0"
          "urllib3==1.26.3"
        ];
      };
      python = forcesPkgs.python38;
    };
    envForces = path "/forces/forces.old.py";
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "forces-config-wrapper";
  template = path "/makes/packages/forces/config-wrapper/template.sh";
}
