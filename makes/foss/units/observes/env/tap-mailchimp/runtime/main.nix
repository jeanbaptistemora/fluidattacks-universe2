{ makeTemplate
, inputs
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_mailchimp";
in
makeTemplate {
  name = "observes-env-tap-mailchimp-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      outputs."/observes/env/tap-mailchimp/runtime/python"
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-paginator-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
