{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "utils-env";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/common/utils/gitlab"
      outputs."/common/utils/common"
    ];
  };
  template = ./template.sh;
}
