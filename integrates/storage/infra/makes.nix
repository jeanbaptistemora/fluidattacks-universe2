# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesStorageDev = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/workspaceForTerraformFromEnv/integratesStorage"
          outputs."/secretsForTerraformFromEnv/integratesStorage"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
      integratesStorage = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorage"
          outputs."/secretsForTerraformFromEnv/integratesStorage"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesStorage = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    integratesStorage = {
      branch = "CI_COMMIT_REF_NAME";
    };
  };
  testTerraform = {
    modules = {
      integratesStorage = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/workspaceForTerraformFromEnv/integratesStorage"
          outputs."/secretsForTerraformFromEnv/integratesStorage"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
    };
  };
  workspaceForTerraformFromEnv = {
    modules = {
      integratesStorage = {
        src = "/integrates/storage/infra/src";
        variable = "CI_COMMIT_REF_NAME";
        version = "1.0";
      };
    };
  };
}
