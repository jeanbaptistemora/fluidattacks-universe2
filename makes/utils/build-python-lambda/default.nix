path: pkgs:

{ dependencies ? [ ]
, name
, python
, requirements
, source
}:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path pkgs;
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
in
makeDerivation {
  arguments = {
    envRequirements = buildPythonRequirements {
      inherit dependencies;
      inherit name;
      inherit python;
      inherit requirements;
    };
    envSource = source;
  };
  builder = path "/makes/utils/build-python-lambda/builder.sh";
  name = "build-python-lambda-for-${name}";
  searchPaths = {
    envPaths = [ pkgs.zip ];
  };
}
