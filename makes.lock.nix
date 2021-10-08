let
  lock = builtins.fromJSON (builtins.readFile ./flake.lock);
in
{
  makesSrc = builtins.fetchTarball {
    url = lock.nodes.makes.locked.url;
    sha256 = lock.nodes.makes.locked.narHash;
  };
}
