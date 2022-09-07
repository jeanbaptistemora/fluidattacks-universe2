# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  lintWithAjv = {
    "common/criteria/compliance" = {
      schema = "/common/criteria/src/compliance/schema.json";
      targets = ["/common/criteria/src/compliance/data.yaml"];
    };
    "common/criteria/requirements" = {
      schema = "/common/criteria/src/requirements/schema.json";
      targets = ["/common/criteria/src/requirements/data.yaml"];
    };
    "common/criteria/vulnerabilities" = {
      schema = "/common/criteria/src/vulnerabilities/schema.json";
      targets = ["/common/criteria/src/vulnerabilities/data.yaml"];
    };
  };
}
