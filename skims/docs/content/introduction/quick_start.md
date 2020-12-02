
## Quick Start

1.  Install Nix as explained in the [tutorial](https://nixos.org/download.html).
1.  Run the following command:

    `nix-env -i product -f 'https://gitlab.com/fluidattacks/product/-/archive/master/product-master.tar.gz'`

1.  You should be able to execute skims now:

    `skims --help`

1. Should you wish to uninstall please run:

    `nix-env -e product`
