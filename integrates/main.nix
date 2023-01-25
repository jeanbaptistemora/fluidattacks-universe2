{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    mprocs --config __argMprocs__
  '';
  name = "integrates";
  replace.__argMprocs__ = ./mprocs.yaml;
  searchPaths.bin = [
    inputs.nixpkgs.mprocs
    outputs."/integrates/back"
    outputs."/integrates/db"
    outputs."/integrates/front"
    outputs."/integrates/storage/dev"
  ];
}
