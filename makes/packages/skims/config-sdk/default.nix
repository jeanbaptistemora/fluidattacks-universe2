{ applications
, path
, makeTemplate
, ...
}:
makeTemplate {
  arguments = {
    envManifestFindingsDev = path "/skims/manifests/findings.dev.json";
    envManifestFindingsProd = "/skims/manifests/findings.prod.json";
    envManifestFindingsStaging = "/skims/manifests/findings.staging.json";
    envSkimsBin = applications.skims;
  };
  name = "skims-config-sdk";
  searchPaths = {
    envPythonPaths = [
      (path "/skims/skims/sdk")
    ];
  };
  template = ''
    export SKIMS_FINDINGS_DEV='__envManifestFindingsDev__'
    export SKIMS_FINDINGS_PROD='__envManifestFindingsProd__'
    export SKIMS_FINDINGS_STAGING='__envManifestFindingsStaging__'
    export SKIMS_BIN='__envSkimsBin__'
  '';
}
