{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  name = "utils-common";
  searchPaths.bin = [ inputs.nixpkgs.coreutils ];
  template = ./template.sh;
}
