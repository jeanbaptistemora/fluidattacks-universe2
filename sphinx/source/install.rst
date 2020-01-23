==========
Installing
==========

``Fluid Asserts`` is hosted on `PyPI <https://pypi.org/project/fluidasserts/>`_,
so you can install it easily using ``pip3``
on a system with ``Python 3``: ::

   $ pip3 install -U fluidasserts

For normal/interactive usage,
you should set the environment variable ``FA_STRICT`` to false
(see below). In an ``UNIX``-like ``OS``: ::

   $ export FA_STRICT="false"

In Windows:

.. code-block:: none

   > set FA_STRICT="false"

Now you're ready to begin :doc:`testing<usage>` vulnerabilities' closure.

-----------------------------------------------
Installing with `Nix <https://nixos.org/nix/>`_
-----------------------------------------------

We are at the `Official Nixpkgs collection <https://github.com/NixOS/nixpkgs>`_.

#. Install **Nix** as explained `here <https://nixos.org/nix/download.html>`_.:

   On most systems it's enough to run:

   .. code-block:: bash

      $ curl https://nixos.org/nix/install | sh
#. Add the **NixOS** channel:

   .. code-block:: bash

      $ nix-channel --add https://nixos.org/channels/nixos-unstable
#. Install **fluidasserts**:

   .. code-block:: bash

      $ nix-env -i fluidasserts
#. Get into a shell with **fluidasserts**!

   .. code-block:: bash

      $ nix-shell -p fluidasserts

-------------------------
Inside a Docker container
-------------------------

If you have ``Docker`` you can check out and run ``Asserts``
inside a container. Just ::

   $ docker pull fluidattacks/asserts

And then go inside the container: ::

   $ docker run -it fluidattacks/asserts sh
   / # asserts

.. literalinclude:: example/banner-only.exp.out

Make sure to do the ``docker pull`` before every ``docker run``
to ensure you are running the latest ``Asserts`` version.

From inside the container you could run ``Asserts``
from the python interactive shell,
or quickly whip up a script using ``vi``.
But it would be much more useful to `mount`
the directory where your exploits live into the container: ::

  $ docker run -v /home/me/myexploits/:/exploits/ -it fluidattacks/asserts sh
  / # asserts /exploits/open-sqli.py

.. literalinclude:: example/qstart-sqli-open.exp.out
   :language: yaml

------------------------------------------------
Inside your CI (Continuous Integration) pipeline
------------------------------------------------

If you have an application subscribed to our
Continuous Hacking Service
which includes the use of ``Asserts``,
you can integrate it into
your ``CI/CD`` pipeline to
ensure that your software builds and ships
with ``no open vulnerabilities``.
We will provide a custom ``Docker`` container
with the specific tests you need
and maintain the build-breaker exploit.

To achieve this, follow these steps:

#. Add the required environment variables
   ``ID`` and ``SECRET``.
   Don't worry, the values will be provided by us!:

   * ``ID``: an identifier that works like your username
   * ``SECRET``: another identifier that works like your password

   For example, in GitLab, your environment would look like this:

   .. figure:: _static/vars.png
      :alt: GitLab environment variables for using Asserts

      GitLab CI environment variables

#. Make sure your execution environment has the required dependencies

   These are:

      * Bash
      * An updated version of Docker

   Please note that using **sh** instead of **bash** is not supported

#. Add a job to run ``Fluid Asserts``.
   For example:

   * in ``GitLab``:

     Add these three lines to
     your ``.gitlab-ci.yml``:

     .. code-block:: yaml

        fluidasserts:
          script:
            - docker pull fluidattacks/break-build
            - bash <(docker run fluidattacks/break-build --static --id ${ID} --secret ${SECRET})

   * in ``Azure DevOps (VSTS)``,

     Add a **Command Line** task with the following script:

     .. code-block:: bash

        docker pull fluidattacks/break-build
        bash <(docker run fluidattacks/break-build --static --id ${ID} --secret ${SECRET})

   * in ``Jenkins``,

     The configuration file should look like this:

     .. code-block:: jenkins

        pipeline {
          agent {
            label 'label'
          }
          environment {
            ID = "test"
            SECRET = "test"
          }
          stages {
            stage('Break Build Static') {
              steps {
                script {
                  sh """
                    docker pull fluidattacks/break-build
                    docker run fluidattacks/break-build --static --id $ {ID} --secret $ {SECRET} | bash
                  """
                }
              }
            }
            stage('Break Build Dynamic') {
              steps {
                script {
                  sh """
                    docker pull fluidattacks/break-build
                    docker run fluidattacks/break-build --dynamic --id $ {ID} --secret $ {SECRET} | bash
                  """
                }
              }
            }
          }
        }

     Please note that while **sh** is the pipeline executor,
     break build commands are piped to **bash**,
     so **bash** is the actual executor

#. Now your pipeline will break
   if any vulnerability is found to be open.
   In order to not break the build,
   but still run the tests,
   add the ``--no-strict`` flag on the command.

#. You can customize the execution

   .. The commands are the following::

   --id ID
      Use this flag to set your user ID
   --secret SECRET
      Use this flag to set your user Secret
   --static
      Run the static container.
   --dynamic
      Run the dynamic container.
   --no-strict
      Don't ``Break the Build`` if any vulnerability is found to be open :(
   --cpus N
      Add this flag to allow execution in N host CPUs (defaults to 1).
      Using **--cpus 0** will use all CPUs in the host
   --no-image-rm
      Use this flag to indicate that you do not want to
      delete images after execution
   --no-container-rm
      Use this flag to indicate that you do not want to
      delete containers after execution,
      (for security reasons, containers should always be removed)
   --color
      Colorize the execution output,
      (in some environments colorizing the output makes the output unreadable)

~~~~~~~~~
CI stages
~~~~~~~~~

OK, I'm in. But in what stage should I test my app with ``Asserts``?

Let's think for a moment in the following architecture

Locally:

#. Develop an amazing feature
#. Push your code to the repository

Inside the continuous integration:

#. Test the code
#. Build the code
#. Deploy an ephemeral environment
#. Make a Pull/Merge Request
#. Deploy the production environment

There are at least four good moments to perform closure testing.

* just after pushing your code to the repository
* after deploying to a staging or ephemeral environment
* after deploying to the production environment
* even after every single commit!

_______________
Post-production
_______________

Just as before, we log in to the artifacts repository,
pull the custom image and run it with ``Docker``.
This job is run only in the ``master`` branch and
in one of the latest stages, namely ``asserts-prod``.

.. code-block:: yaml

   asserts-production:
     stage: asserts-prod
     script:
       - docker pull fluidattacks/break-build
       - bash <(docker run fluidattacks/break-build --dynamic --id ${ID} --secret ${SECRET})
     retry: 2
     only:
       - master

_______________
Post-ephemeral
_______________

But wait! We could catch bugs before deploying to production.
If you use `ephemeral environments
<https://en.wikipedia.org/wiki/Deployment_environment#Staging>`_,
you can also perform closure testing in those:

.. code-block:: yaml

   Asserts-Review:
     stage: asserts-post-ephemeral
     script:
       - docker pull fluidattacks/break-build
       - bash <(docker run fluidattacks/break-build --dynamic --id ${ID} --secret ${SECRET})
     retry: 2
     except:
       - master
       - triggers

In contrast to the post-deploy job above,
this one runs on the development branches,
during the ``asserts-post-ephemeral`` stage.
Otherwise, everything else is the same,
just like staging environments mirror production environments.

____________________________
Just after pushing your code
____________________________

We can start catching bugs even only with the source code:

.. code-block:: yaml

   Asserts-Review:
     stage: asserts-code-test
     script:
       - docker pull fluidattacks/break-build
       - bash <(docker run fluidattacks/break-build --static --id ${ID} --secret ${SECRET})
     except:
       - master
       - triggers

In contrast to the post-ephemeral job above,
this one runs on the development branches,
during the ``asserts-code-test`` stage,
over the source code only.

__________
Pre-commit
__________

As a developer you might be thinking
"why wait until all other CI stages are finished
if I just want to test whether my last commit
fixed the security hole?"
You `could` just run ``Asserts`` in your development machine,
but sometimes tiny details (like dependencies versions)
might cause the testing to pass in your machine
but fail continuous integration.

In that case you might run
the ``Dockerized`` incarnation of ``Asserts``
as a ``pre-commit`` hook:

.. code-block:: yaml

   - id: asserts-docker
     name: Running Asserts on the code
     description: Run Asserts to perform SAST
     entry: -v /path/to/your/code/:/code fluidattacks/asserts:latest /code/asserts.sh
     language: docker_image

This particular configuration is for the ``pre-commit`` tool,
but can be adapted for similar tools like ``overcommit``.
The use of such tools is convenient for the developer,
as tests can be quickly run in their machine with every commit:

   .. figure:: _static/pre-commit-ok.png
      :alt: Pre-commit pass

      Pre-commit test passed

   .. figure:: _static/pre-commit-fail.png
      :alt: Pre-commit fail

      Pre-commit test fails. Commiting is not allowed!

The same tests can also be run in CI time
(for example, in a ``lint`` stage)
to ensure that nothing is broken,
even if the developer forgot to run it.
Just

.. code-block:: none

  - pre-commit run --all-files

somewhere in your ``CI`` script.
