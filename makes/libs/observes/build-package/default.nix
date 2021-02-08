{ nixPkgs
, packageConfig
, path
, python
}:
let
  buildPythonReqs = import (path "/makes/utils/build-python-requirements") path nixPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path nixPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path nixPkgs;
  reqs = buildPythonReqs {
    inherit python;
    name = packageConfig.packageName;
    dependencies = packageConfig.buildInputsList;
    requirements = {
      direct = packageConfig.pythonReqs.direct;
      inherited = packageConfig.pythonReqs.inherited;
    };
  };
in
makeTemplate {
  arguments = {
    envPackageSrc = packageConfig.projectDir;
    envPythonRequirements = reqs;
    envSearchPaths = makeSearchPaths packageConfig.buildInputsList;
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "observes-package-${packageConfig.packageName}";
  template = path "/makes/libs/observes/build-package/setup-package.sh";
}
