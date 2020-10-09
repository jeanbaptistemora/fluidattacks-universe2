let
  pkgs = import ../pkgs/skims.nix;
  sortsDependencies = import ../src/sorts-dependencies.nix pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        sortsDependencies.build
        sortsDependencies.runtime
      ];

      # Constants for dynamic linked binaries
      LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
    })
  )
