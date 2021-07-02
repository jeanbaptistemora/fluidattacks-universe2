{ applications
, path
, makeTemplate
, ...
}:
makeTemplate {
  arguments = {
    envManifestFindings = path "/skims/manifests/findings.json";
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
    export SKIMS_FINDINGS='__envManifestFindings__'
  '';
}
