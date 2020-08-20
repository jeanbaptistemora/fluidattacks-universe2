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
    url = "https://gitlab.com/fluidattacks/public/-/raw/61dc81795a5613ae402f1e047b478a31ebe61688/shared-scripts/sops.sh";
    sha256 = "18kyzsq78gwkr22r992p2b4n6zx58j0vc9z2c95ss7svbhn418m2";
  };
}
