# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lintWithAjv = {
    "common/compute/arch/sizes" = {
      schema = "/common/compute/arch/sizes/schema.json";
      targets = ["/common/compute/arch/sizes/data.yaml"];
    };
  };
}
