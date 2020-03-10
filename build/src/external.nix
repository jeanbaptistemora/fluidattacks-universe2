pkgs:

rec {
  srcExternalGitlabVariables = pkgs.fetchurl {
    url = "https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh";
    sha256 = "13y7xd9n0859lgncljxbkgvdhx9akxflkarcv4klsn9cqz3mgr06";
  };
  srcExternalMail = pkgs.fetchurl {
    url = "https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/mail.py";
    sha256 = "1a7kki53qxdwfh5s6043ygnyzk0liszxn4fygzfkwx7nhsmdf6k3";
  };
  srcExternalSops = pkgs.fetchurl {
    url = "https://static-objects.gitlab.net/fluidattacks/public/raw/master/shared-scripts/sops.sh";
    sha256 = "0alm1k5dj5fvcdyygm9bk58kgpkjnzl2k7p7d5if5cw8j8bi32rb";
  };
}
