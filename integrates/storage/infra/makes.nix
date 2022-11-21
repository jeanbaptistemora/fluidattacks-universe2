# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesStorage = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
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
  testTerraform = {
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
}
