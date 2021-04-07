{ makeTemplate
, path
, ...
}:
let
  self = path "/observes/common/singer_io";
in
makeTemplate {
  name = "observes-env-runtime-singer-io";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
  };
}
