==============
Firing up VPNs
==============

Requirements
============

#. A real linux (WSL is not enough) (a Virtual Machine does ok)

Steps
=====

#. Clone the continuous repository `here <https://gitlab.com/fluidattacks/continuous>`_.

#. Install Nix, as explained `here <https://nixos.org/nix/download.html>`_.

   On most systems:

   .. code:: sh

       $ curl https://nixos.org/nix/install | sh

#. Run the local VPN script for your project :)

   In the case of the project **foo**

   .. code:: sh

       continuous$ ./vpns/foo.sh

   At this point, the script will start the VPN and connect to it.

   Please keep the VPN shell alive while you hack,
   and hit ctrl + c when you want to stop the service.

#. Hack hack hack.
