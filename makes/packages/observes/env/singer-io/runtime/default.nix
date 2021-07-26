{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/common/singer_io";
in
makeTemplate {
  name = "observes-env-singer-io-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      singer-io.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      singer-io.runtime.python
    ];
  };
}
