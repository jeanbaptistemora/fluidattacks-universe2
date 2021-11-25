{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-zoho-crm-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-zoho-crm-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/singer/tap-zoho-crm/env/runtime"
    ];
  };
}
