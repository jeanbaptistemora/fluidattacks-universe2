{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argManifests__ = ./k8s;
  };
  searchPaths = {
    bin = [inputs.nixpkgs.utillinux];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/integrates/back/deploy/lib"
    ];
  };
  name = "integrates-back-deploy-prod";
  entrypoint = ./entrypoint.sh;
}
