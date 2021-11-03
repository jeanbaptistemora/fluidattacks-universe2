{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.jq
      inputs.nixpkgs.sops
    ];
  };
  name = "utils-bash-lib-sops";
  template = ./template.sh;
}
