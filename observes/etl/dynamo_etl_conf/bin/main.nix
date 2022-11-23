{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  system = "x86_64-linux";
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  env = pkg.outputs.packages."${system}".env.bin;
in
  makeScript {
    entrypoint = "dynamo-etl \"\${@}\"";
    searchPaths = {
      bin = [env];
    };
    name = "dynamo-etl";
  }
