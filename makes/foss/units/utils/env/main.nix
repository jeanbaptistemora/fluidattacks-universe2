{ inputs
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "utils-env";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/utils/gitlab"
      outputs."/utils/common"
    ];
  };
  template = ./template.sh;
}
