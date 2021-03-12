{ buildPythonPackage
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-runtime-singer-io";
  searchPaths = {
    envPython38Paths = [
      self
    ];
  };
}
