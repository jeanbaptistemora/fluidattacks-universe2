{
  inputs,
  makeTemplate,
  ...
}:
makeTemplate {
  searchPaths.bin = [
    inputs.nixpkgs.gnugrep
    inputs.nixpkgs.jq
  ];
  name = "utils-lint-npm-deps";
  template = ./template.sh;
}
