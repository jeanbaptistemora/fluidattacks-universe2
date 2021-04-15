{ nixpkgs3
, ...
}:
let
  ext = publisher: name: version: sha256:
    builtins.trace
      "https://marketplace.visualstudio.com/items?itemName=${publisher}.${name} ${version}"
      { inherit name publisher sha256 version; };

  nixpkgs = nixpkgs3;
in
nixpkgs.vscode-with-extensions.override {
  vscodeExtensions = nixpkgs.vscode-utils.extensionsFromVscodeMarketplace [
    (ext "eamodio" "gitlens" "11.3.0" "m2Zn+e6hj59SujcW5ptdrYDrc4CviZ4wyCndO2BhyF8=")
    (ext "mads-hartmann" "bash-ide-vscode" "1.11.0" "d7acWLdRW8nVjQPU5iln9hl9zUx61XN4lvmFLbwLBMM=")
    (ext "4ops" "terraform" "0.2.1" "r5W5S9hIn4AlVtr6y7HoVwtJqZ+vYQgukj/ehJQRwKQ=")
  ] ++ [
    nixpkgs.vscode-extensions.bbenoist.Nix
    nixpkgs.vscode-extensions.haskell.haskell
    nixpkgs.vscode-extensions.justusadam.language-haskell
    nixpkgs.vscode-extensions.ms-azuretools.vscode-docker
    nixpkgs.vscode-extensions.ms-python.python
    nixpkgs.vscode-extensions.ms-python.vscode-pylance
    nixpkgs.vscode-extensions.streetsidesoftware.code-spell-checker
  ];
}
