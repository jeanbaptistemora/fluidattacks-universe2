{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/common/paginator";
in
makeTemplate {
  name = "observes-env-paginator-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      paginator.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      paginator.runtime.python
    ];
  };
}
