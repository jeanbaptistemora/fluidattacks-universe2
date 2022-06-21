fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  python_version = "python310";
  nixpkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "5iKbUlOVY9nFWiN2Y6NUpQ3ogXOVrGi1TBANqvcB3ys=";
  };
  out = import ./. {
    inherit observesIndex nixpkgs projectPath python_version system;
    src = ./.;
  };
in
  out
