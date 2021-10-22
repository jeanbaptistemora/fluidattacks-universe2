{ makeTemplate
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
      outputs."/observes/env/singer-io/runtime"
      outputs."/observes/env/paginator/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
