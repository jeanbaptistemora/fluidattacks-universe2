{ nixPkgs
, packageConfig
, path
}:
let
  buildPythonReqs = import (path "/makes/utils/build-python-requirements") path nixPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path nixPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path nixPkgs;
  reqs = buildPythonReqs {
    name = packageConfig.packageName;
    dependencies = packageConfig.buildInputsList;
    python = packageConfig.python;
    requirements = {
      direct = packageConfig.reqs.python.direct;
      inherited = packageConfig.reqs.python.inherited;
    };
  };
in
makeTemplate {
  arguments = {
    envPackageSrc = packageConfig.srcPath;
    envPythonReqs = reqs;
    envSearchPaths = makeSearchPaths packageConfig.buildInputsList;
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "observes-package-${packageConfig.packageName}";
  template = path "/makes/libs/observes/build-package/setup-package.sh";
}
