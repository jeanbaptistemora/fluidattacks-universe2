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
    bin = [
      inputs.nixpkgs.jq
      inputs.nixpkgs.python39
    ];
    source = [outputs."/secretsForEnvFromSops/commonOkta"];
  };
  template = ''
    export OKTA_DATA=$(python __argParser__ | jq -rc .) \
      && unset OKTA_DATA_RAW
  '';
  name = "okta-parse";
}
