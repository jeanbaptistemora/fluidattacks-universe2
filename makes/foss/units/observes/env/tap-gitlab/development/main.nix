{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-gitlab-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-gitlab-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/tap-gitlab/runtime"
    ];
  };
}
