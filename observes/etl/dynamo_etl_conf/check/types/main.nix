{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  system = "x86_64-linux";
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  check = pkg.outputs.packages."${system}".check.types;
in
  makeTemplate {
    searchPaths = {
      bin = [check];
    };
    name = "observes-etl-dynamo-etl-conf-check-types";
  }
