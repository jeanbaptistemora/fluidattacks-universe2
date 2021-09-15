{ inputs
, makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/makes/foss/modules/makes/okta/src/parser/__init__.py";
  };
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [
      outputs."/secretsForAwsFromEnv/makesDev"
      outputs."/secretsForEnvFromSops/makesOktaData"
    ];
  };
  template = ''
    export OKTA_DATA=$(python __argParser__)
  '';
  name = "okta-parse";
}
