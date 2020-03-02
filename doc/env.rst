======================
Continuous environment
======================

There's a base environment that you can setup easily to have:

#. `Fluid Asserts <https://fluidattacks.com/asserts>`_.

   A Framework to verify security assumptions.

#. The `Continuous Toolbox <https://fluidattacks.gitlab.io/continuous/reference.html>`_.

   A swiss tool to develop **Asserts**'s exploits with high quality,
   run them,
   get their vulnerabilities,
   report findings to Integrates via API,
   and in general, to control, manage and deploy the entire
   `Break Build Service <https://fluidattacks.com/asserts/install/#inside-your-ci-continuous-integration-pipeline>`_.

Requirements
============

#. Clone the continuous repository `here <https://gitlab.com/fluidattacks/continuous>`_.

#. Setup your local ci as explained :doc:`here<ci>`.

#. Execute the following command:

   .. code:: sh

       continuous/build/shells/continuous $ nix-shell

   You'll be dropped into a shell with the same properties of a normal shell
   (same filesystem, same hardware, same Internet config, etc),
   but with the tools mentioned above.
