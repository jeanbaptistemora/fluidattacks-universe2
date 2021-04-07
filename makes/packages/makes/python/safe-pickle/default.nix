{ makeTemplate
, path
, nixpkgs
, ...
}:
makeTemplate {
  arguments = {
    envSrcSkimsSkims = path "/skims/skims";
  };
  name = "skims-config-runtime";
  searchPaths = {
    envPythonPaths = [
      (path "/makes/packages/makes/python/safe-pickle/src")
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.python-dateutil
    ];
  };
  template = path "/makes/packages/skims/config-runtime/template.sh";
}
