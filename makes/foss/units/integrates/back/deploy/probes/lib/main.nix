{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  name = "integrates-back-probes-lib";
  searchPaths.bin = [
    inputs.nixpkgs.awscli
    inputs.nixpkgs.curl
    inputs.nixpkgs.gnugrep
  ];
  template = ./template.sh;
}
