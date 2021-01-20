_: pkgs:

derivations: {
  binPath = pkgs.lib.strings.makeBinPath derivations;
  libPath = pkgs.lib.strings.makeLibraryPath derivations;
  pyPath = builtins.concatStringsSep ":" [
    (pkgs.lib.strings.makeSearchPath "lib/python3.8/site-packages" derivations)
    (pkgs.lib.strings.makeSearchPath "lib/python3.7/site-packages" derivations)
  ];
}
