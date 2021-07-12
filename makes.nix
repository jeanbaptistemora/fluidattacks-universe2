# For more information visit:
# https://github.com/fluidattacks/makes
{
  imports = [
    ./forces/makes.nix
    ./integrates/makes.nix
    ./makes/makes.nix
    ./skims/makes.nix
  ];
  inputs = {
    product = import ./.;
  };
  requiredMakesVersion = "21.09";
}
