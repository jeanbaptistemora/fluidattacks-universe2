{ makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  replace = {
    __argManifestFindings__ = projectPath "/skims/manifests/findings.json";
    __argManifestQueues__ = projectPath "/skims/manifests/queues.json";
    __argSkimsProcessGroupOnAws__ =
      outputs."/computeOnAwsBatch/skimsProcessGroup";
  };
  name = "skims-config-sdk";
  searchPaths = {
    pythonPackage = [
      (projectPath "/skims/skims/sdk")
    ];
  };
  template = ''
    export SKIMS_FINDINGS='__argManifestFindings__'
    export SKIMS_PROCESS_GROUP_ON_AWS='__argSkimsProcessGroupOnAws__/bin/compute-on-aws-batch-for-skimsProcessGroup'
    export SKIMS_QUEUES='__argManifestQueues__'
  '';
}
