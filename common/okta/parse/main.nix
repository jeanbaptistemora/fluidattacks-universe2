# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/common/okta/parse/src/__init__.py";
    __argSopsData__ = projectPath "/common/okta/data.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      inputs.nixpkgs.python39
      inputs.nixpkgs.sops
    ];
  };
  template = ./template.sh;
  name = "okta-parse";
}
