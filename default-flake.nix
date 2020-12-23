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
  # nix-env -qa -f ./default-flake.nix
  # nix-env -i skims-bin -f ./default-flake.nix
  flake.defaultNix.outputs.packages.x86_64-linux
