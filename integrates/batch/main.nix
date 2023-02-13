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
      inputs.nixpkgs.roboto
      inputs.nixpkgs.roboto-mono
      inputs.nixpkgs.ruby
      inputs.nixpkgs.openssl
      inputs.nixpkgs.nix
      outputs."/integrates/db"
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/env"
      outputs."/integrates/storage/dev/lib/populate"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
