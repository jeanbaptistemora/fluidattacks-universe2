{ packages
, path
, makeTemplate
, ...
}:
makeTemplate {
  name = "skims-config-sdk";
  searchPaths = {
    envPaths = [ packages.skims ];
    envPython38Paths = [
      (path "/skims/skims/sdk")
    ];
  };
}
