# For more information visit:
# https://github.com/fluidattacks/makes
{
  imports = [
    ./forces/makes.nix
    ./makes/makes.nix
  ];
  inputs = {
    product = import ./.;
  };
  requiredMakesVersion = "21.08";
}
