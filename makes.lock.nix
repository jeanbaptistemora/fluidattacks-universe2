# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "4d4be139c2ff92c3b4db5c5d27c77124b5985900";
  };
}
