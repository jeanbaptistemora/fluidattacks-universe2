{ makeTemplate
, path
, nixpkgs
, ...
}:
makeTemplate {
  name = "makes-python-safe-pickle";
  searchPaths = {
    envPythonPaths = [
      (path "/makes/packages/makes/python/safe-pickle/src")
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.python-dateutil
    ];
  };
}
