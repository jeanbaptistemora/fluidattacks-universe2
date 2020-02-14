let
  asFile = builtins.toFile "src";
in rec {
  etcGroup = asFile ''
      root:x:0:
      nixbld:x:30000:nixbld1,nixbld2,nixbld3,nixbld4,nixbld5,nixbld6
  '';

  etcGshadow = asFile ''
      root:x::
      nixbld:!::nixbld1,nixbld2,nixbld3,nixbld4,nixbld5,nixbld6
  '';

  etcLoginDefs = asFile ''
  '';

  etcNixNixConf = asFile ''
    sandbox = false
  '';

  etcNssConf = asFile ''
    hosts: dns files
  '';

  etcPamdOther = asFile ''
    account sufficient pam_unix.so
    auth sufficient pam_rootok.so
    password requisite pam_unix.so nullok sha512
    session required pam_unix.so
  '';

  etcPasswd = asFile ''
      root:x:0:0::/root:/bin/bash
      nixbld1:x:30001:30000::/var/empty:/bin/bash
      nixbld2:x:30002:30000::/var/empty:/bin/bash
      nixbld3:x:30003:30000::/var/empty:/bin/bash
      nixbld4:x:30004:30000::/var/empty:/bin/bash
      nixbld5:x:30005:30000::/var/empty:/bin/bash
      nixbld6:x:30006:30000::/var/empty:/bin/bash
  '';

  etcShadow = asFile ''
      root:!x:::::::
      nixbld1:!:18242::::::
      nixbld2:!:18242::::::
      nixbld3:!:18242::::::
      nixbld4:!:18242::::::
      nixbld5:!:18242::::::
      nixbld6:!:18242::::::
  '';

  rootNixChannels = asFile ''
    https://nixos.org/channels/nixpkgs-unstable nixpkgs
  '';

  rootNixDefExpr = import ../../../../../pkgs/stable-src.nix;
}
