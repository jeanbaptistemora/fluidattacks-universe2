{ inputs
, makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
makeTemplate {
  replace = {
    __argSrcForces__ = projectPath "/forces";
  };
  name = "forces-config-runtime";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.python38
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "forces-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    pythonPackage = [
      (projectPath "/forces")
    ];
  };
  template = projectPath "/makes/foss/units/forces/config-runtime/template.sh";
}
