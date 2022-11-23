=====
Usage
=====

Most of ``Fluid Asserts`` functions for the end-user
are `predicates` regarding a specific vulnerability.
In that sense,
you "ask" ``Asserts``
whether a certain `Target of Evaluation`
has an open vulnerability of some type or
if it has been closed.

``Asserts`` replies by telling you
that the status of the vulnerability is
`OPEN` or `CLOSED` plus
additional info, such as
why it thinks the flaw is or is not still there,
where it is found,
when it was tested,
and the `fingerprint` (the gory details of the transaction).

-------------
SQL Injection
-------------

To verify that
a SQL injection is still open,
you can write a script like this:

.. literalinclude:: example/qstart-sqli-open.exp

Then run it:

.. code-block:: shell-session

   $ asserts open_sqli.py

.. literalinclude:: example/qstart-sqli-open.exp.out
    :language: yaml

To verify that a SQL injection is closed,
use the same function:

.. literalinclude:: example/qstart-sqli-closed.exp

.. code-block:: shell-session

   $ asserts closed_sqli.py

.. literalinclude:: example/qstart-sqli-closed.exp.out
    :language: yaml

------------------------------
Cross-Site Scripting (``XSS``)
------------------------------

The function :func:`.has_xss` requires
a few more parameters:

.. literalinclude:: example/qstart-xss-open.exp

.. code-block:: shell-session

   $ asserts open_xss.py

.. literalinclude:: example/qstart-xss-open.exp.out
    :language: yaml

To test if
an ``XSS`` vulnerability has been closed:

.. literalinclude:: example/qstart-xss-closed.exp

.. code-block:: shell-session

   $ asserts closed_xss.py

.. literalinclude:: example/qstart-xss-closed.exp.out
    :language: yaml
