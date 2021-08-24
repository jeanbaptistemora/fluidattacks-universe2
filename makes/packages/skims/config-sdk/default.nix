{ applications
, path
, makeTemplate
, ...
}:
makeTemplate {
  arguments = {
    envManifestFindings = path "/skims/manifests/findings.json";
    envManifestQueues = path "/skims/manifests/queues.json";
    envSkimsProcessGroupOnAws = applications.skims.process-group-on-aws;
  };
  name = "skims-config-sdk";
  searchPaths = {
    envPythonPaths = [
      (path "/skims/skims/sdk")
    ];
  };
  template = ''
    export SKIMS_FINDINGS='__envManifestFindings__'
    export SKIMS_PROCESS_GROUP_ON_AWS='__envSkimsProcessGroupOnAws__'
    export SKIMS_QUEUES='__envManifestQueues__'
  '';
}
