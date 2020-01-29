``Fluid Asserts`` is an engine
to automate the closing of security findings
over execution environments (``DAST``).

Setup
=====

.. code-block:: text

   pip install -U fluidasserts

Usage
=====

Import the required ``Fluid Asserts`` modules into your exploit:

.. code-block:: python

   from fluidasserts.proto import http

   http.has_sqli('http://testphp.vulnweb.com/AJAX/infoartist.php?id=3%27')

And run your exploit:

.. code-block:: text

   $ python example.py
   ---
   # Fluid Asserts (v. 18.5.39870)
   #  ___
   # | >>|> fluid
   # |___|  attacks, we hack your software
   #
   # Loading attack modules ...
   ---
   check: fluidasserts.proto.http.has_sqli
   status: OPEN
   message: 'A bad text was present: "Warning.*mysql_.*"'
   details:
     fingerprint:
       sha256: 2778b9d49ae98527b95f1c60b0989c1ee870c11e65ee6c359eff8b6f757b0e27
       banner: "Server: nginx/1.4.1\r\nDate: Mon, 26 Jan 1970 01:11:40 GMT\r\nContent-Type:\
         \ text/xml\r\nTransfer-Encoding: chunked\r\nConnection: keep-alive\r\nX-Powered-By:\
         \ PHP/5.3.10-1~lucid+2uwsgi2"
     url: http://testphp.vulnweb.com/AJAX/infoartist.php?id=3%27
   when: 2018-05-28 11:40:19.721614
   ---
