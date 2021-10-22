{ makeTemplate
, inputs
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
      inputs.product.observes-env-postgres-client-runtime
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
