{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_mixpanel";
in
makeTemplate {
  name = "observes-env-tap-mixpanel-runtime";
  searchPaths = {
    envLibraries = [
      nixpkgs.gcc.cc.lib
    ];
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-mixpanel.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-mixpanel.runtime.python
    ];
    envSources = [
      singer-io.runtime
    ];
  };
}
