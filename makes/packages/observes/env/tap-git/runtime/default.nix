{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_git";
in
makeTemplate {
  name = "observes-env-tap-git-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.git
      tap-git.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-git.runtime.python
    ];
  };
}
