{
  inputs,
  makeTemplate,
  ...
}:
makeTemplate {
  searchPaths.bin = [
    inputs.nixpkgs.coreutils
    inputs.nixpkgs.envsubst
    inputs.nixpkgs.kubectl
    inputs.nixpkgs.yq
    inputs.nixpkgs.gnugrep
  ];
  name = "integrates-back-deploy-lib";
  template = ./template.sh;
}
