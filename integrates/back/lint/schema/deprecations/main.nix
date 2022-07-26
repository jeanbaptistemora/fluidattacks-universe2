{
  inputs,
  makeDerivation,
  projectPath,
  ...
}:
makeDerivation {
  searchPaths.bin = [
    inputs.nixpkgs.python39
  ];
  builder = ./builder.sh;
  env.envSrc = projectPath "/integrates/back/lint/schema/deprecations/";
  name = "integrates-back-lint-schema-deprecations";
}
