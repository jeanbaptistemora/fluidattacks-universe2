{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-service-timedoctor-tokens";
    packagePath = path "/observes/services/timedoctor_tokens";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-service-timedoctor-tokens-runtime";
  searchPaths = {
    envPython38Paths = [
      packages.observes.env.service-timedoctor-tokens.runtime.python
      self
    ];
  };
}
