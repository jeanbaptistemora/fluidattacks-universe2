# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "22c92c3993c95e783db3ba10af6e4e3d3f91f5c8";
  };
}
