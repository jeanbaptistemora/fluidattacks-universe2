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
