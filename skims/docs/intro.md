# Installing

0.  Install Nix as explained in the [tutorial](https://nixos.org/download.html).
0.  Run the following command:

    `nix-env -i product -f 'https://gitlab.com/fluidattacks/product/-/archive/master/integrates-master.tar.gz'`

0.  You should be able to execute skims now:

    `skims --help`

0. Should you wish to uninstall please run:

    `nix-env -e product`
