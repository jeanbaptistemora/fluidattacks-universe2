==========
Installing
==========

``Fluid Asserts`` can be installed with the following command: ::

   $ bash <(curl -L fluidattacks.com/install/asserts)

Now you're ready to begin :doc:`testing<usage>` vulnerabilities' closure.

Alternatively you can execute a container image with the container runtime
of your preference: ::

   $ podman run -it fluidattacks/asserts  # with Podman
   $ docker run -it fluidattacks/asserts  # with Docker

.. literalinclude:: example/banner-only.exp.out

In order to `mount` the directory where your exploits live into the container: ::

  $ podman run -v /path/to/my/exploits:/exploits -it fluidattacks/asserts /exploits/open-sqli.py
  $ docker run -v /path/to/my/exploits:/exploits -it fluidattacks/asserts /exploits/open-sqli.py

.. literalinclude:: example/qstart-sqli-open.exp.out
   :language: yaml
