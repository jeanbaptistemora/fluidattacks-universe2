======================================
Welcome to Continuous's documentation!
======================================

Here you can find plenty of information regarding the continuous-hacking
process and tools.

.. toctree::
   :hidden:
   :caption: Navigation

   Home <self>
   ci
   env
   secrets
   vpns
   break_build_admin
   reference

===================
Structure and files
===================

The directory structure is (only the most important directories are included):

  - **subscriptions:** Contains all active continuous subscriptions.
  - **suspended:** Contains all suspended continuous subscriptions.
  - **finished:** Contains all finished continuous subscriptions.
  - **break-build:** Contains all source code for break-build service.
  - **toolbox:** Contains all source code for the Fluid CLI.

There are ``4`` folders within every subscription:

  - **break-build:** You can assume a subscription does not have
    the service if this folder is missing.

    - **static:** Source code asserts exploits for break-build.
    - **dynamic:** Application/infrastructure asserts exploits for break-build.


  - **config:**

    - **config.yml:** File for non-sensitive configurations like
      source code repositories, customer, cloning method, vpn, etc.
    - **secrets.yaml:** File for secrets like users, passwords, repo ssh keys, etc.


  - **toe:**

    - :ref:`lines-csv` File for tracking
      which source code lines have been reviewed.
    - :ref:`inputs-csv` File for tracking
      which application/infrastructure inputs
      have been reviewed.

  - **fusion:** This folder does not come by default.
    It contains the source code of the subscription repositories
    and can be obtained by cloning it with the :ref:`Fluid CLI <repo-cloning>`.

==========================
Target of Evaluation (ToE)
==========================

It consists of lines and fields
(see `Fluid Rules <https://fluidattacks.com/web/en/rules/>`_)
that must be tested.

.. _lines-csv:

+++++++++
lines.csv
+++++++++

The file ``lines.csv`` has detailed data about
reviewed and pending-to-review lines of
source code. It allows analysts
to focus on reviewing lines that haven't
been tested yet.

It contains the following columns:

+-----------------+--------------------------------------------------+------------------------------------+
| **Column**      | **Description**                                  | **Example**                        |
+-----------------+--------------------------------------------------+------------------------------------+
| filename        | Path of a file from the fusion directory         | repo/path/weak.php                 |
+-----------------+--------------------------------------------------+------------------------------------+
| loc             | | Lines of code of such file,                    | 1593                               |
|                 | | it does not include comments                   |                                    |
+-----------------+--------------------------------------------------+------------------------------------+
| tested-lines    | | Number of lines that                           | 865                                |
|                 | | have already been reviewed                     |                                    |
+-----------------+--------------------------------------------------+------------------------------------+
| modified-date   | | Last modification date of file                 | 2018-12-19                         |
|                 | | detected by git in ``YYYY-MM-DD`` format       |                                    |
+-----------------+--------------------------------------------------+------------------------------------+
| modified-commit | | Hash of the last commit                        | 51d4b3c                            |
|                 | | that modified the file                         |                                    |
+-----------------+--------------------------------------------------+------------------------------------+
| tested-date     | | Date in which the file was last reviewed       | 2019-05-21                         |
|                 | | by ``Fluid Attacks`` in ``YYYY-MM-DD`` format. |                                    |
|                 | | If new changes to the file are commited,       |                                    |
|                 | | the date changes to 2000-01-01                 |                                    |
+-----------------+--------------------------------------------------+------------------------------------+
| comments        | Found vulnerabilities in the file                | UseOfHardCodedCredentials(CWE-798) |
+-----------------+--------------------------------------------------+------------------------------------+

``lines.csv`` files must comply with the rules
defined in ``templates/lines.csv``.

.. _inputs-csv:

++++++++++
inputs.csv
++++++++++

Just like ``lines.csv``, the ``inputs.csv`` file
is a list of all the dynamic inputs contained
in the subscription application.

+---------------+------------------------------------------------+------------------------------------+
| **Column**    | **Description**                                | **Example**                        |
+---------------+------------------------------------------------+------------------------------------+
| component     | URL where the input to be tested is located    | www.myapp.net/login                |
+---------------+------------------------------------------------+------------------------------------+
| entry_point   | | Name of the input to be tested.              | | username,                        |
|               | | It can be a field, header, port,             | | HTTP/POST/Request,               |
|               | | cookie, etc.                                 | | session                          |
+---------------+------------------------------------------------+------------------------------------+
| verified      | | Indicates if the entry was already tested.   | Yes                                |
|               | | The only valid values are ``Yes`` and ``No`` |                                    |
+---------------+------------------------------------------------+------------------------------------+
| commit        | | Last commit that modified the input.         | b3e01c9                            |
|               | | Using ``fingerprint.py`` is recommended      |                                    |
+---------------+------------------------------------------------+------------------------------------+
| date          | Last revision date in ``YYYY-MM-DD`` format    | 2019-03-14                         |
+---------------+------------------------------------------------+------------------------------------+
| vulns         | Found vulnerabilities in the input             | InformationExposure(CWE-200)       |
+---------------+------------------------------------------------+------------------------------------+
| modified_date | | Last modification date of the entry          | UseOfHardCodedCredentials(CWE-798) |
|               | | in ``YYYY-MM-DD`` format                     |                                    |
+---------------+------------------------------------------------+------------------------------------+

``inputs.csv`` files must comply with the rules
defined in ``templates/inputs.csv``.

=====
Tools
=====

Before you use any of the following tools,
please install the lastest version of
`SOPS <https://github.com/mozilla/sops/releases>`_.

SOPS is a secret encrypting tool developed by Mozilla
that allows analysts to decrypt the ``config/secrets.yaml``
of the subscriptions they have access to.

+++++++++++++++
Fluid CLI
+++++++++++++++
FLuid CLI is a software, which makes the hacker's job easier by
providing the tools they need in continuous testing.

You can access more documentation about it :ref:`here <api-reference>`.

.. _repo-cloning:

+++++++++++++++
1. Repo-cloning
+++++++++++++++

This script allows analysts to clone all
the repositories associated to a specific subscription
as long as they have access to it in Okta.

Execute the following command from the continuous repo root:

.. code:: bash

  continuous$ fluid resources --clone <subscription-name>

This one could also be executed inside the selected subscription folder

.. code:: bash

  continuous/subscriptions/subscription$ fluid resources --clone

This command will ask for okta credentials.

Once permissions get validated, a fusion folder is created with all
repositories from the selected subscription

This command could also be used for updating repositories in case
they have changed

+++++++++++++++
2. Update-lines
+++++++++++++++

As source code git respositories from all subscriptions
are being constantly updated,
the ``lines.csv`` must be kept updated with such changes.
By using ``update-lines.py``,
analysts can syncronize their local ``lines.csv``
with the latest changes made in subscription's repositories.
In order to update your ``lines.csv``,
you have to:

- Clone or update the subscription's
  source code with ``repo-cloning``.

- Run:

  .. code:: bash

    continuous/subscriptions/subscription$ ../../tools3/update_lines.py

+++++++++++++++++++
3. Evaluated-so far
+++++++++++++++++++

As commit messages must follow a
`standard <https://gitlab.com/fluidattacks/continuous/wikis/Commit-and-MR-Messages>`_,
The ``evaluated_so_far.py`` script automatically generates
a valid commit message based on chages made
to the ``lines.csv`` and ``inputs.csv`` files during tests.

.. code:: bash

  continuous/subscriptions/<subscription>$ fluid drills --generate-commit-msg


++++++++++++++
4. Fingerprint
++++++++++++++

Allows to extract information
from already cloned repositories
using ``repo-cloning``.
It provides repository name,
last commit hash and date,
among others.

.. code:: bash

  continuous/subscriptions/<subscription>$ fluid resources --fingerprint

+++++++++++++++
5. Source Clear
+++++++++++++++

Tool used for Static Analysis Security Testing (``SAST``)
on the source code of subscriptions.
Usage:

- Install `Docker <https://docs.docker.com/install/>`_

- Log in to ``Gitlab Container Registry``:

  .. code:: bash

    docker login registry.gitlab.com

- Preparare the container:

  .. code:: bash

    user@PC:~/continuous$ docker run --name=sourceclear -v $(pwd):/continuous \
    --rm -i -t registry.gitlab.com/fluidattacks/continuous:srcclr bash

- Once inside the container, run:

  .. code:: bash

    srcclr activate
    cd /continuous
    srcclr scan --recursive --allow-dirty subscriptions/subscription/fusion

===
VPN
===

Some subscriptions need a ``VPN``
for either accessing their applications
or cloning their source code.
In oder to access a subscription ``VPN``:

- Run the following command to install Nix:

  .. code:: bash

    userPC:~/continuous/$ curl https://nixos.org/nix/install | sh

- Run:

  .. code:: bash

    userPC:~/continuous/$ ./vpns/subscription.sh

After running this command,
you will be inside a nix-shell
that is connected to the subscription's VPN.
