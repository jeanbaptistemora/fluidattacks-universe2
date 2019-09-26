============
Requirements
============

-------
Summary
-------

~~~~~~~~~~~~~
In a computer
~~~~~~~~~~~~~

On a modern operating system, all you need is Python 3.7 or higher.

If installing on a very barebones operating system,
make sure you have
``curl``, ``make``, ``gcc``
and the libraries
``libc``, ``libffi``, ``openssl``, and ``jpeg``.

~~~~~~~~~~~~~~~~~~~
In a CI environment
~~~~~~~~~~~~~~~~~~~

All you need is support for Docker CE 17 or higher.

On Windows, you also need ``HyperV`` support.

~~~~~~~~
Hardware
~~~~~~~~

* CPU: 4 cores @1.8GHz
* RAM: 4GiB DDR3 @1.6Ghz
* Disk space: 10GiB

-------
Details
-------

~~~~~~~~~~~
For Windows
~~~~~~~~~~~

If you don't have any of the above requirements,
but you are on a recent version of Windows,
you can install everything using `Chocolatey <https://chocolatey.org/>`_.
There are many ways to perform each step, and
we will list only one here.
Refer to the links for alternatives and details.

1. Open an `administrative shell <https://www.howtogeek.com/194041/how-to-open-the-command-prompt-as-administrator-in-windows-8.1/>`_.
   Probably the easiest way to do this
   is hit :kbd:`Windows+R`,
   type in ``cmd`` and then
   hit :kbd:`Control+Shift+Enter`
   to ensure it is run as administrator.

2. Once in the shell,
   `run this command <https://chocolatey.org/docs/installation#install-with-cmdexe>`_:

.. code-block:: console

   > @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" ^
   -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ^
   ((New-Object System.Net.WebClient).^
   DownloadString('https://chocolatey.org/install.ps1'))" ^
   && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

3. Now install Python 3:

.. code-block:: console

   > choco install python3

4. Refresh the environment
   so you can call ``python`` and ``pip``
   from the command line directly:

.. code-block:: console

   > refreshenv

5. Now you can :doc:`install <install>` ``Asserts`` as usual.
