# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{outputs, ...}: {
  imports = [
    ./parse/makes.nix
  ];
  deployTerraform = {
    modules = {
      commonOkta = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/common/okta/parse"
          outputs."/secretsForTerraformFromEnv/commonOkta"
        ];
        src = "/common/okta/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonOkta = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/common/okta/parse"
          outputs."/secretsForTerraformFromEnv/commonOkta"
        ];
        src = "/common/okta/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    commonOkta = {
      oktaApiToken = "OKTA_API_TOKEN";
      oktaDataApps = "OKTA_DATA_APPS";
      oktaDataGroups = "OKTA_DATA_GROUPS";
      oktaDataRules = "OKTA_DATA_RULES";
      oktaDataUsers = "OKTA_DATA_USERS";
      oktaDataAppGroups = "OKTA_DATA_APP_GROUPS";
      oktaDataAppUsers = "OKTA_DATA_APP_USERS";
      oktaDataAwsGroupRoles = "OKTA_DATA_AWS_GROUP_ROLES";
      oktaDataAwsUserRoles = "OKTA_DATA_AWS_USER_ROLES";
    };
  };
  testTerraform = {
    modules = {
      commonOkta = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/common/okta/parse"
          outputs."/secretsForTerraformFromEnv/commonOkta"
        ];
        src = "/common/okta/infra";
        version = "1.0";
      };
    };
  };
}
