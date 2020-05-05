let
  pkgs = import ../pkgs/stable.nix;

  builders.rubyGem = import ../builders/ruby-gem pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.sysctl
        pkgs.nodejs
        pkgs.awscli
        pkgs.curl
        pkgs.cacert
        pkgs.sops
        pkgs.git
      ];

      rubyGemFastlane =
        builders.rubyGem "fastlane:2.146.1";
    })
  )
