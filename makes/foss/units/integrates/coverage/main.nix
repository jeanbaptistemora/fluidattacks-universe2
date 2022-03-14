{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "integrates-coverage";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.git
      inputs.nixpkgs.python39Packages.codecov
      inputs.nixpkgs.python39Packages.coverage
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/coverage/entrypoint.sh";
}
