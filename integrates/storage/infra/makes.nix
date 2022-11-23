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
