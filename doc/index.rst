=========================================
Welcome to Fluid Services' documentation!
=========================================

.. toctree::
   :hidden:
   :caption: Navigation

   Home <self>
   ci
   drills_vpns
   forces_exploits
   forces_admin

===================
Structure and files
===================

The directory structure is (only the most important directories are included):

  - **build:** Source code for the build system
  - **forces:** Contains all source code for forces service.
  - **subscriptions:** Contains all active subscriptions.
  - **toolbox:** Contains all source code for the Fluid CLI.

There are ``4`` folders within every subscription:

  - **forces:** You can assume a subscription does not have
    the service if this folder is missing.

    - **static:** Source code asserts exploits for forces.
    - **dynamic:** Application/infrastructure asserts exploits for forces.


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

  - **fusion:**

    - This folder does not come by default.
      It contains the source code of the subscription repositories
      and can be obtained as shown in later steps of this tutorial.

==========================
Target of Evaluation (ToE)
==========================

It consists of lines and fields
(see `Fluid Rules <https://fluidattacks.com/web/rules/>`_)
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

=====
Tools
=====

All tools you may need can be installed in your system with:

.. code:: bash

    continuous$ ./install.sh

It's the official way, and the only one we support.

+++++++++
Fluid CLI
+++++++++

Bundle of scripts for daily operations:

.. code:: bash

    continuous$ fluid --help

+++++++++++++
FLuid Asserts
+++++++++++++

`Hacking framework and knowledge library <https://fluidattacks.com/asserts/>`_.

.. code:: bash

    continuous$ asserts --help

======================
Hacking and Exploiting
======================

Ask an administrator to grant you the corresponding **Okta** roles
depending on the subscriptions you are assigned to.
Having privileges is the starting point of the following tutorial.

+++++++++
Resources
+++++++++

In order to hack you need the customer's source code,
you can have it or update it with:

.. code:: bash

    continuous$ fluid resources --pull-repos <subscription-name>

Please do so at least once a day, before hacking and everything else

+++++++++++++++
Toe-Enumeration
+++++++++++++++

As source code gets updated by the customer,
the ``lines.csv`` and ``inputs.csv`` must be kept updated with such changes.

The first step is to enumerate the ToE, this will update the ``lines.csv`` file:

.. code:: bash

    continuous$ fluid drills --update-lines <subscription>

Once you hack the ToE,
manually modify these files to indicate which lines and inputs where tested.

While updating the ``inputs.csv``,
computing the commit and dates of modification of an input can be obtained with:

.. code:: bash

  continuous$ fluid resources --fingerprint

++++++++++
Exploiting
++++++++++

Please refer to the `Exploits Documentation <forces_exploits.html>`__
for further information.

+++++++++++++++++++++
Commit and MR Message
+++++++++++++++++++++

Every day, at the end, you must commit the changes you made.

All commit messages must follow the
`Commit and MR Standard <https://gitlab.com/fluidattacks/continuous/wikis/Commit-and-MR-Messages>`_,
this tool will help you with the math:

.. code:: bash

  continuous$ fluid drills --generate-commit-msg <subscription>

++++++++++++
Source Clear
++++++++++++

Use this for Static Analysis Security Testing (``SAST``)
on the source code of subscriptions.
Usage:

- Install `Docker <https://docs.docker.com/install/>`_

- Log in to ``Gitlab Container Registry``:

  .. code:: bash

    continuous$ docker login registry.gitlab.com
    continuous$ docker run -i -t --rm \
      --name sourceclear \
      --volume "$(pwd):/continuous" \
      registry.gitlab.com/fluidattacks/continuous:srcclr bash

- Once inside the container, run:

  .. code:: bash

    srcclr activate
    cd /continuous
    srcclr scan --recursive --allow-dirty subscriptions/subscription/fusion

  You can obtain the asked token by login-in to **Source Clear** through Okta.
