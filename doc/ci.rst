======================
Continuous Integration
======================

Our `CI System <https://gitlab.com/fluidattacks/continuous/blob/master/.gitlab-ci.yml>`_
can be **run locally**.

Requirements
============

#. A real linux (WSL is not enough) (a Virtual Machine does ok)

Steps
=====

#. Clone the `repository <https://gitlab.com/fluidattacks/continuous>`_.

#. Install `Nix <https://nixos.org/nix/download.html>`_.

   On most systems:

   .. code:: sh

       $ curl https://nixos.org/nix/install | sh

#. Run the local CI script :)

   .. code:: sh

       continuous$ ./build.sh

   At this point, the script will start fetching the base packages for you.

   It may take some time, relax.

   In the meantime a nice idea is to visit
   `Integrates <https://fluidattacks.com/index>`_
   and issue your **Integrates API Token**.

   You'll find it useful.

#. Finally, commit your changes and create a
   `Merge Request <https://gitlab.com/fluidattacks/continuous/merge_requests>`_
