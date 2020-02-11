pkgs:

let
  modules.docker.images.nixos.nix = import ../../nixos/nix pkgs;
  modules.build.dependencies =  import ../../../../build/dependencies pkgs;
in
  pkgs.dockerTools.buildImage {
    name = "local";
    tag = "nix";

    fromImage = modules.docker.images.nixos.nix;

    contents = modules.build.dependencies;

    config = {
      Cmd = [ "/usr/bin/env" "bash" ];
      Env = [
        "ENV=/etc/profile"
        "GIT_SSL_CAINFO=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt"
        "USER=root"
        "NIX_PATH=/nix/var/nix/profiles/per-user/root/channels"
        "NIX_SSL_CERT_FILE=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt"
        "PATH=/nix/var/nix/profiles/default/bin:/nix/var/nix/profiles/default/sbin:/bin:/sbin:/usr/bin:/usr/sbin"
      ];
      WorkingDir = "/";
    };
  }
