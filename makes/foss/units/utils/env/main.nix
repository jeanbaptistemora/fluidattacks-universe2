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
      (outputs."/utils/gitlab")
    ];
  };
  template = ./template.sh;
}
