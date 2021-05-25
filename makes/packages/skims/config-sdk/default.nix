{ applications
, path
, makeTemplate
, ...
}:
makeTemplate {
  arguments = {
    envSkimsBin = applications.skims;
  };
  name = "skims-config-sdk";
  searchPaths = {
    envPythonPaths = [
      (path "/skims/skims/sdk")
    ];
  };
  template = ''
    export SKIMS_BIN='__envSkimsBin__'
  '';
}
