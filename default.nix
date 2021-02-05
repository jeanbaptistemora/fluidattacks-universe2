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
      name = builtins.replaceStrings [ "/bin" "/" ] [ "" "-" ] name;
      value = flake.defaultNix.outputs.packages.x86_64-linux.${name};
    })
    [
      "forces/bin"
      "integrates/back/bin"
      "integrates/back/probes/liveness"
      "integrates/back/probes/readiness"
      "integrates/cache/bin"
      "integrates/db/bin"
      "integrates/storage/bin"
      "makes/wait/bin"
      "melts/bin"
      "skims/bin"
      "sorts/bin"
    ]
  );

  # Nix2 components (deprecated)
  legacyComponents = {
    product = import ./default-legacy.nix;
  };
in
components // legacyComponents
