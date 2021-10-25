{ makePythonPypiEnvironment
, makeTemplate
, inputs
, ...
}:
let
  pythonRequirements = makePythonPypiEnvironment {
    name = "melts-development";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  name = "melts-config-development";
  searchPaths = {
    bin = [ inputs.nixpkgs.docker ];
    source = [ pythonRequirements ];
  };
}
