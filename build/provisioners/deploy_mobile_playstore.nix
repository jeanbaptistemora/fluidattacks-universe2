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
        pkgs.awscli
        pkgs.cacert
        pkgs.git
        pkgs.ruby
        pkgs.sops
      ];

      rubyGemBundler =
        builders.rubyGem "bundler:2.1.4";
    })
  )
