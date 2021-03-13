{ makeDerivation
, makeOci
, nixpkgs
, path
, ...
}:
makeOci {
  config = {
    Env = [
      "GIT_SSL_CAINFO=/etc/ssl/certs/ca-bundle.crt"
      "HOME=/home/makes"
      "NIX_PATH=/nix/var/nix/profiles/per-user/makes/channels"
      "NIX_SSL_CERT_FILE=/etc/ssl/certs/ca-bundle.crt"
      "PATH=/bin:/nix/var/nix/profiles/default/bin"
      "SSL_CERT_FILE=/etc/ssl/certs/ca-bundle.crt"
      "SYSTEM_CERTIFICATE_PATH=/etc/ssl/certs/ca-bundle.crt"
      "USER=makes"
    ];
    User = "makes:makes";
    WorkingDir = "/product";
  };
  contents = [
    (makeDerivation {
      arguments = {
        envEtcGroup = ''
          makes:x:0:
        '';
        envEtcGshadow = ''
          makes:*::
        '';
        envEtcPamdOther = ''
          account sufficient pam_unix.so
          auth sufficient pam_rootok.so
          password requisite pam_unix.so nullok sha512
          session required pam_unix.so
        '';
        envEtcPasswd = ''
          makes:x:0:0::/home/makes:${nixpkgs.bash}/bin/bash
        '';
        envEtcShadow = ''
          makes:!x:::::::
        '';
        envSrc = path "/";
      };
      builder = path "/makes/packages/makes/oci/builder.sh";
      name = "makes-oci-customization-layer";
    })
    nixpkgs.bash
    nixpkgs.cacert
    nixpkgs.coreutils
    nixpkgs.git
    nixpkgs.gnutar
    nixpkgs.gzip
    nixpkgs.nix
  ];
}
