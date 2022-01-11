{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-gitlab-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-gitlab-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."${inputs.observesIndex.tap.gitlab.env.runtime}"
    ];
  };
}
