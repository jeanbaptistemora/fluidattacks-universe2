# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{outputs, ...}: {
  deployTerraform = {
    modules = {
      sorts = {
        setup = [outputs."/secretsForAwsFromGitlab/prodSorts"];
        src = "/sorts/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      sorts = {
        setup = [outputs."/secretsForAwsFromGitlab/dev"];
        src = "/sorts/infra/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      sorts = {
        setup = [outputs."/secretsForAwsFromGitlab/dev"];
        src = "/sorts/infra/src";
        version = "1.0";
      };
    };
  };
}
