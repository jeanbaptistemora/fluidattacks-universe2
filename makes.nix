# For more information visit:
# https://github.com/fluidattacks/makes
{ fetchNixpkgs
, projectPath
, ...
}:
{
  cache = {
    readAndWrite = {
      enable = true;
      name = "fluidattacks";
      pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
    };
  };
  extendingMakesDir = "/makes/foss/units";
  imports = [
    ./makes/foss/modules/makes.nix
  ];
  inputs = {
    nixpkgs = fetchNixpkgs {
      rev = "f88fc7a04249cf230377dd11e04bf125d45e9abe";
      sha256 = "1dkwcsgwyi76s1dqbrxll83a232h9ljwn4cps88w9fam68rf8qv3";
    };
    product = import (projectPath "/");
  };
}
