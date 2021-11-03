{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
    ];
    source = [
      (inputs.legacy.importUtility "env")
    ];
  };
  name = "utils-bash-lib-aws";
  template = ./template.sh;
}
