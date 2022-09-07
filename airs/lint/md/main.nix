# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  ...
}:
makeTemplate {
  replace = {
    __argAcceptedKeywordsFile__ = ./acepted_keywords.lst;
  };
  name = "airs-lint-md";
  searchPaths = {
    bin = [
      inputs.nixpkgs.diction
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.pcre
    ];
  };
  template = ./template.sh;
}
