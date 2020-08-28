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
}
