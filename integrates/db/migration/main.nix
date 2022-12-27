{
  makeScript,
  outputs,
  inputs,
  ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.ffmpeg
    ];
  };
  name = "integrates-db-migration";
  entrypoint = ./entrypoint.sh;
}
