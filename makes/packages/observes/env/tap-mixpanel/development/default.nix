{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-mixpanel;
  singerIO = buildPythonPackage {
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-tap-mixpanel";
    packagePath = path "/observes/singer/tap_mixpanel";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    envPaths = [
      pkgEnv.development.python
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.pandas
      pkgEnv.development.python
      singerIO
      self
    ];
  };
}
