{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-batch";
  searchPaths = {
    bin = [
      inputs.nixpkgs.noto-fonts
      inputs.nixpkgs.python39
      inputs.nixpkgs.roboto
      inputs.nixpkgs.roboto-mono
      inputs.nixpkgs.ruby
      inputs.nixpkgs.openssl
      outputs."/integrates/db"
      outputs."/integrates/storage"
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
