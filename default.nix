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
  components = {
    forces = flake.defaultNix.outputs.packages.x86_64-linux."forces/bin";
    melts = flake.defaultNix.outputs.packages.x86_64-linux."melts/bin";
    skims = flake.defaultNix.outputs.packages.x86_64-linux."skims/bin";
    sorts = flake.defaultNix.outputs.packages.x86_64-linux."sorts/bin";
  };

  # Nix2 components (deprecated)
  legacyComponents = {
    product = import ./default-legacy.nix;
  };
in
components // legacyComponents
