{ packages
, path
, makeTemplate
, ...
}:
makeTemplate {
  name = "skims-config-sdk";
  searchPaths = {
    envPaths = [ packages.skims ];
    envPythonPaths = [
      (path "/skims/skims/sdk")
    ];
  };
}
