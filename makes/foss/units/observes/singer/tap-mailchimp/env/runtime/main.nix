{ makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_mailchimp";
in
makeTemplate {
  name = "observes-singer-tap-mailchimp-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      outputs."/observes/singer/tap-mailchimp/env/runtime/python"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/common/paginator/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
