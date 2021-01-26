{ buildInputs ? [ ], nixPkgs, path, packageName, projectDir, python, pythonReqs }:
let
  buildPythonReqs = import (path "/makes/utils/build-python-requirements") path nixPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path nixPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path nixPkgs;
  reqs = buildPythonReqs {
    inherit python;
    dependencies = buildInputs;
    requirements = {
      direct = pythonReqs.direct;
      inherited = pythonReqs.inherited;
    };
  };
in
makeTemplate {
  arguments = {
    envPythonRequirements = reqs;
    envPackageName = packageName;
    envPackageSrc = projectDir;
    envSearchPaths = makeSearchPaths buildInputs;
    envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
  };
  name = "observes-package-${packageName}";
  template = path "/makes/utils/observes-lib/build-package/setup-package.sh";
}
