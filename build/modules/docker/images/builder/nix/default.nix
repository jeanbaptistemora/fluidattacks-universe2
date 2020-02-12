let
  pkgs = import ../../../../../pkgs/stable.nix;
  modules.build.dependencies = import ../../../../../dependencies pkgs;
in
  pkgs.dockerTools.buildImage {
    name = "builder";
    tag = "nix";

    fromImage = import ../../nixos/nix;

    contents = modules.build.dependencies.all;

    config = {
      Cmd = [ "/usr/bin/env" "bash" ];
      Env = [
        "ENV=/etc/profile"
        "GIT_SSL_CAINFO=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt"
        "NIX_PATH=/nix/var/nix/profiles/per-user/root/channels"
        "NIX_SSL_CERT_FILE=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt"
        "PATH=/nix/var/nix/profiles/default/bin:/nix/var/nix/profiles/default/sbin:/bin:/sbin:/usr/bin:/usr/sbin"
        "USER=root"
      ];
      WorkingDir = "/";
    };
  }
