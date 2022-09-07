# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      skims = {
        setup = [outputs."/secretsForAwsFromGitlab/prodSkims"];
        src = "/skims/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      skims = {
        setup = [outputs."/secretsForAwsFromGitlab/dev"];
        src = "/skims/infra/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      skims = {
        setup = [outputs."/secretsForAwsFromGitlab/dev"];
        src = "/skims/infra/src";
        version = "1.0";
      };
    };
  };
}
