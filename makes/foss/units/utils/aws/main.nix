{ inputs
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
    ];
    source = [
      outputs."/utils/env"
    ];
  };
  name = "utils-bash-lib-aws";
  template = ./template.sh;
}
