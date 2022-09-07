# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
  ];
  lintMarkdown = {
    docs = {
      config = "/docs/.lint-markdown.rb";
      targets = ["/docs/src/docs"];
    };
  };
  secretsForAwsFromGitlab = {
    prodDocs = {
      roleArn = "arn:aws:iam::205810638802:role/prod_docs";
      duration = 3600;
    };
  };
}
