# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/tags/22.09";
  };
}
