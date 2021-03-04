{ nixPkgs
, packageConfig
, path
}:
let
  buildPythonReqs = import (path "/makes/utils/build-python-requirements") path nixPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path nixPkgs;

  inheritedBuildInputs = builtins.foldl' (a: b: a ++ b) [ ] (
    builtins.map (pkg: pkg.buildInputs) packageConfig.reqs.local
  );
  inheritedPythonEnvs = builtins.map (pkg: pkg.python_env) packageConfig.reqs.local;
  inheritedPythonSrcs = builtins.map (pkg: pkg.packagePath) packageConfig.reqs.local;

  python_env = buildPythonReqs {
    name = packageConfig.packageName;
    dependencies = packageConfig.buildInputs ++ inheritedBuildInputs;
    python = packageConfig.python;
    requirements = {
      direct = packageConfig.reqs.python.direct;
      inherited = packageConfig.reqs.python.inherited;
    };
  };

  bInputs = packageConfig.buildInputs ++ inheritedBuildInputs;

  template = makeTemplate {
    arguments = {
      envPythonReqsEnvs = [ python_env ] ++ inheritedPythonEnvs;
      envPythonReqsSrcs = [ packageConfig.srcPath ] ++ inheritedPythonSrcs;
      envUtilsBashLibPython = path "/makes/utils/python/template.sh";
    };
    searchPaths = {
      envPaths = bInputs;
      envLibraries = bInputs;
      envPython37Paths = bInputs;
      envPython38Paths = bInputs;
    };
    name = "observes-package-${packageConfig.packageName}";
    template = path "/makes/libs/observes/build-package/setup-package.sh";
  };
in
{
  inherit python_env template;
  name = packageConfig.packageName;
  packagePath = packageConfig.srcPath;
  buildInputs = [ template ] ++ packageConfig.buildInputs ++ inheritedBuildInputs;
}
