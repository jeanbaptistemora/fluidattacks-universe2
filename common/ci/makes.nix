# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.bash
      inputs.nixpkgs.git
      inputs.nixpkgs.jq
    ];
  };
in {
  deployTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCiProd"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCiDev"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonCiProd = {
      vars = [
        "BUILDKITE_API_TOKEN"
        "GITLAB_TOKEN_FLUIDATTACKS"
      ];
      manifest = "/common/secrets/prod.yaml";
    };
    commonCiDev = {
      vars = [
        "BUILDKITE_API_TOKEN"
        "GITLAB_TOKEN_FLUIDATTACKS"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonCi = {
      buildkiteApiToken = "BUILDKITE_API_TOKEN";
      gitlabTokenFluidattacks = "GITLAB_TOKEN_FLUIDATTACKS";
    };
  };
  testTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCiDev"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
}
