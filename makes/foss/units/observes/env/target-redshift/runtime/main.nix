{ makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/target_redshift";
in
makeTemplate {
  name = "observes-env-target-redshift-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      outputs."/observes/env/target-redshift/runtime/python"
      outputs."/observes/env/postgres-client/runtime"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
