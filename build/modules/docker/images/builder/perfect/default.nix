let
  pkgs = import ../../../../../pkgs/stable.nix;

  modules.build.dependencies = import ../../../../../dependencies pkgs;

  src = import ./src.nix;
in
  with pkgs;

  dockerTools.buildLayeredImage {
    name = "builder";
    tag = "perfect";
    created = "now";

    contents = modules.build.dependencies.all;
    maxLayers = 125;

    # Literally create an OS from scratch lol
    extraCommands = ''
      #! ${bash}
      set -eux

      chmod +w ./etc

      mkdir ./etc/nix
      mkdir ./etc/pam.d
      mkdir ./tmp
      mkdir ./usr
      mkdir ./usr/bin
      mkdir ./root
      mkdir ./root/.nix-defexpr
      mkdir ./root/.nix-defexpr/channels

      ln -s ${coreutils}/bin/env ./usr/bin

      cp -r ${src.etcGroup} ./etc/group
      cp -r ${src.etcGshadow} ./etc/gshadow
      cp -r ${src.etcLoginDefs} ./etc/login.defs
      cp -r ${src.etcNixNixConf} ./etc/nix/nix.conf
      cp -r ${src.etcNssConf} ./etc/nsswitch.conf
      cp -r ${src.etcPamdOther} ./etc/pam.d/other
      cp -r ${src.etcPasswd} ./etc/passwd
      cp -r ${src.etcShadow} ./etc/shadow
      cp -r ${src.rootNixChannels} ./root/.nix-channels
      cp -r ${src.rootNixDefExpr} ./root/.nix-defexpr/channels/nixpkgs
    '';

    config = {
      Cmd = [ "/bin/bash" ];
      Env = [
        "ENV=/etc/profile"
        "GIT_SSL_CAINFO=${cacert}/etc/ssl/certs/ca-bundle.crt"
        "NIX_PATH=/root/.nix-defexpr/channels"
        "NIX_SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt"
        "PATH=/bin:/usr/bin"
        "USER=root"
      ];
      WorkingDir = "/";
    };
  }
