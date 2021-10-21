{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-streamer-zoho-crm-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-streamer-zoho-crm-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/streamer-zoho-crm/runtime"
    ];
  };
}
