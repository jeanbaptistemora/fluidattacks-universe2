# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argManifests__ = projectPath "/integrates/back/deploy/dev/k8s";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.envsubst
      inputs.nixpkgs.kubectl
      inputs.nixpkgs.utillinux
      inputs.nixpkgs.yq
      inputs.nixpkgs.gnugrep
    ];
    source = [
      outputs."/common/utils/aws"
    ];
  };
  name = "integrates-back-deploy-dev";
  entrypoint = ./entrypoint.sh;
}
