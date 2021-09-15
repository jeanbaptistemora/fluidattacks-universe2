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
    config = "/makes/foss/modules/all/lint-git-commit-msg-config.js";
    parser = "/makes/foss/modules/all/lint-git-commit-msg-parser.js";
  };
  lintGitMailMap = {
    enable = true;
  };
  lintNix = {
    enable = true;
    targets = [ "/" ];
  };
  lintTerraform = {
    config = "/makes/foss/modules/all/lint-terraform-config.hcl";
  };
}
