{ nixpkgs
, ...
}:
let
  ext = publisher: name: version: sha256:
    builtins.trace
      "https://marketplace.visualstudio.com/items?itemName=${publisher}.${name} ${version}"
      { inherit name publisher sha256 version; };
in
nixpkgs.vscode-with-extensions.override {
  vscodeExtensions = nixpkgs.vscode-utils.extensionsFromVscodeMarketplace [
    (ext "bbenoist" "Nix" "1.0.1" "qwxqOGublQeVP2qrLF94ndX/Be9oZOn+ZMCFX1yyoH0=")
    (ext "eamodio" "gitlens" "11.3.0" "m2Zn+e6hj59SujcW5ptdrYDrc4CviZ4wyCndO2BhyF8=")
    (ext "haskell" "haskell" "1.2.0" "nv7jFpIobEA7ZOeY1E7jLDEC0L6RkXvLxSrYIzSxum8=")
    (ext "justusadam" "language-haskell" "3.4.0" "/pidWbyT+hgH7GslVAYK1u5RJmMSvMqj6nKq/mWpZyk=")
    (ext "mads-hartmann" "bash-ide-vscode" "1.11.0" "d7acWLdRW8nVjQPU5iln9hl9zUx61XN4lvmFLbwLBMM=")
    (ext "ms-azuretools" "vscode-docker" "1.11.0" "2W2CkrZFCPfGAWy/SHsVRGlveSWyMb5sUZjqziQAKJA=")
    (ext "ms-python" "python" "2021.3.680753044" "xVed3KCc1IbNKVlW5Wc2XWDT/pyIKMS5cNTzK6fOM6g=")
    (ext "ms-python" "vscode-pylance" "2021.3.3" "fxbl+u4HDe3ZVW8FCJdqDyNm3kLNRnryz+ApsXmovok=")
    (ext "4ops" "terraform" "0.2.1" "r5W5S9hIn4AlVtr6y7HoVwtJqZ+vYQgukj/ehJQRwKQ=")
  ];
}
