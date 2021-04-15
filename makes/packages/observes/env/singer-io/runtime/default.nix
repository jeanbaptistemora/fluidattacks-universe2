{ makeTemplate
, path
, ...
}:
let
  self = path "/observes/common/singer_io";
in
makeTemplate {
  name = "observes-env-singer-io-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
  };
}
