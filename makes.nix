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
    ./makes/config/forces/makes.nix
    ./makes/config/integrates/makes.nix
    ./makes/config/makes/makes.nix
    ./makes/config/skims/makes.nix
    ./makes/config/all/makes.nix
  ];
  inputs = {
    product = import (path "/");
  };
  requiredMakesVersion = "21.08";
}
