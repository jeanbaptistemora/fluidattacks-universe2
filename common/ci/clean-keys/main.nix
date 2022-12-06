{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "common-ci-clean-keys";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/common/utils/aws"
    ];
  };

  entrypoint = ./entrypoint.sh;
}
