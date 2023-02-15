{
  imports = [
    ./dev/makes.nix
    ./lint/makes.nix
  ];
  securePythonWithBandit = {
    integratesBack = {
      python = "3.11";
      target = "/integrates/back/src";
    };
  };
}
