let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ [
          pkgs.git
          pkgs.glibcLocales
          pkgs.diction
          pkgs.file
          pkgs.pcre
        ];
    })
  )
