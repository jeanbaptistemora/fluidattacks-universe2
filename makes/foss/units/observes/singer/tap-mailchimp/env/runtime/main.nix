{ inputs
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.tap.mailchimp.root;
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
      outputs."${inputs.observesIndex.tap.mailchimp.env.runtime}/python"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/common/paginator/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
