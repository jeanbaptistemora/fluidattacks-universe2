{
  inputs,
  makeScript,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-utils-license";
  searchPaths.bin = [
    inputs.nixpkgs.git
    inputs.nixpkgs.reuse
  ];
}
