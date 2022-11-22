# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesStorageDev = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorageDev"
          outputs."/envVarsForTerraform/integratesStorageDev"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
      integratesStorageProd = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorageProd"
          outputs."/envVarsForTerraform/integratesStorageProd"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
    };
  };
  envVarsForTerraform = {
    integratesStorageDev = {
      endpoint = "integrates-storage-dev";
    };
    integratesStorageProd = {
      endpoint = "integrates-storage-prod";
    };
  };
  lintTerraform = {
    modules = {
      integratesStorageDev = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorageDev"
          outputs."/envVarsForTerraform/integratesStorageDev"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
      integratesStorageProd = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorageProd"
          outputs."/envVarsForTerraform/integratesStorageProd"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesStorageDev = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorageDev"
          outputs."/envVarsForTerraform/integratesStorageDev"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
      integratesStorageProd = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/workspaceForTerraformFromEnv/integratesStorageProd"
          outputs."/envVarsForTerraform/integratesStorageProd"
        ];
        src = "/integrates/storage/infra/src";
        version = "1.0";
      };
    };
  };
  workspaceForTerraformFromEnv = {
    modules = {
      integratesStorageDev = {
        src = "/integrates/storage/infra/src";
        variable = "CI_COMMIT_REF_NAME";
        version = "1.0";
      };
      integratesStorageProd = {
        src = "/integrates/storage/infra/src";
        variable = "";
        version = "1.0";
      };
    };
  };
}
