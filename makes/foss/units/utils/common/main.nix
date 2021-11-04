{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.coreutils
    ];
  };
  name = "utils-common";
  template = ./template.sh;
}
