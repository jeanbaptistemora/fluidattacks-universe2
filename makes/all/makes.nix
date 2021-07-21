# https://github.com/fluidattacks/makes
{
  formatBash = {
    enable = true;
    targets = [ "/" ];
  };
  formatNix = {
    enable = true;
    targets = [ "/" ];
  };
  formatPython = {
    enable = true;
    targets = [ "/" ];
  };
  formatTerraform = {
    enable = true;
    targets = [ "/" ];
  };
  lintBash = {
    enable = true;
    targets = [ "/" ];
  };
  lintGitCommitMsg = {
    branch = "master";
    enable = true;
    config = ./lint-git-commit-msg-config.js;
    parser = ./lint-git-commit-msg-parser.js;
  };
  lintGitMailMap = {
    enable = true;
  };
  lintNix = {
    enable = true;
    targets = [ "/" ];
  };
  lintTerraform = {
    config = ''
      config {
        module = true
      }
      plugin "aws" {
        enabled = true
        deep_check = true
      }
      rule "aws_resource_missing_tags" {
        enabled = true
        tags = [
          "Name",
          "management:type",
          "management:product",
        ]
        exclude = [
          "aws_iam_instance_profile",
          "aws_iam_policy",
        ]
      }
    '';
  };
}
