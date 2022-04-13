{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
    ];
    source = [
      outputs."/common/utils/env"
    ];
  };
  name = "utils-bash-lib-aws";
  template = ./template.sh;
}
