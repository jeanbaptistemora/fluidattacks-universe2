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
      name = builtins.replaceStrings [ "." ] [ "-" ] name;
      value = flake.defaultNix.outputs.packages.x86_64-linux.${name};
    })
    (builtins.filter
      (value: builtins.isString value && value != "")
      (builtins.split "\n" (
        (builtins.readFile ./makes/attrs/applications.lst) +
        (builtins.readFile ./makes/attrs/packages.lst)
      ))
    )
  );

  m = import (import ./makes.lock.nix).makesSrc;
in
components // { inherit m; }
