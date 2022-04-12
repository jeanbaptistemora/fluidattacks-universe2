{
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/common/okta/src/parser/__init__.py";
  };
  searchPaths = {
    bin = [inputs.nixpkgs.python38];
    source = [
      outputs."/secretsForEnvFromSops/commonOktaData"
    ];
  };
  template = ''
    export OKTA_DATA=$(python __argParser__)
  '';
  name = "okta-parse";
}
