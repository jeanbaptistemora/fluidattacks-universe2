# For more information visit:
# https://github.com/fluidattacks/makes
{ path
, ...
}:
{
  cache = {
    enable = true;
    name = "fluidattacks";
    pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
  };
  imports = [
    ./makes/forces/makes.nix
    ./makes/integrates/makes.nix
    ./makes/makes/makes.nix
    ./makes/skims/makes.nix
    ./makes/all/makes.nix
  ];
  inputs = {
    product = import (path "/");
  };
  makesCommit = "0dae5699b8d806e33e18122311c8af9510e18048";
}
