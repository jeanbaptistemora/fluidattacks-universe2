{
  imports = [
    ./dev/makes.nix
    ./lint/makes.nix
  ];
  securePythonWithBandit = {
    integratesBack = {
      python = "3.9";
      target = "/integrates/back/src";
    };
  };
}
