{
  inputs,
  makeScript,
  ...
}:
makeScript {
  name = "common-ci-clean-keys";
  searchPaths.bin = [
    inputs.nixpkgs.awscli
    inputs.nixpkgs.gnugrep
    inputs.nixpkgs.jq
  ];
  entrypoint = ./entrypoint.sh;
}
