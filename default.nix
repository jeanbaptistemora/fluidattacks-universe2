let
  lock = builtins.fromJSON (builtins.readFile ./flake.lock);

  flake = import flakeCompatSrc {
    src = ./.;
  };
  flakeCompatSrc = fetchTarball {
    url = "https://github.com/edolstra/flake-compat/archive/${lock.nodes.flakeCompat.locked.rev}.tar.gz";
    sha256 = lock.nodes.flakeCompat.locked.narHash;
  };
in
  {
    forces = flake.defaultNix.outputs.packages.x86_64-linux.forces-bin;
    melts = flake.defaultNix.outputs.packages.x86_64-linux.melts-bin;
    skims = flake.defaultNix.outputs.packages.x86_64-linux.skims-bin;

    # Legacy binaries live here
    product = import ./default-legacy.nix;
  }
