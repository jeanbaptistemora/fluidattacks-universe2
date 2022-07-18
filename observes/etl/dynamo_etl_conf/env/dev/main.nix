{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  system = "x86_64-linux";
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  env = pkg.outputs.packages."${system}".env.dev;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-etl-dynamo-etl-conf-env-dev";
  }
