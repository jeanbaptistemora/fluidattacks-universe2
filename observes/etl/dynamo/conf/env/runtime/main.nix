{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  env = pkg.outputs.packages.x86_64-linux.env.bin;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-etl-dynamo-conf-env-runtime";
  }
