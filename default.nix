let
  lock = builtins.fromJSON (builtins.readFile ./flake.lock);

  flake = import flakeCompatSrc {
    src = ./.;
  };
  flakeCompatSrc = fetchTarball {
    url = "https://github.com/edolstra/flake-compat/archive/${lock.nodes.flakeCompat.locked.rev}.tar.gz";
    sha256 = lock.nodes.flakeCompat.locked.narHash;
  };

  # Flake components
  components = builtins.listToAttrs (builtins.map
    (name: {
      name = builtins.replaceStrings [ "/" ] [ "-" ] name;
      value = flake.defaultNix.outputs.packages.x86_64-linux.${name};
    })
    [
      "forces"
      "integrates/back"
      "integrates/back/probes/liveness"
      "integrates/back/probes/readiness"
      "integrates/cache"
      "integrates/db"
      "integrates/storage"
      "makes/wait"
      "melts"
      "skims"
      "sorts"
    ]
  );

  # Nix2 components (deprecated)
  legacyComponents = {
    product = import ./default-legacy.nix;
  };
in
components // legacyComponents
